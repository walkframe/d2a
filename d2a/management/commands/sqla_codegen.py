
import importlib
import inspect
import logging
import sys
from collections import OrderedDict

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models.fields import NOT_PROVIDED
from django.template import Context, Template
from django.template.loader import get_template
from django.utils import timezone
from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import TypeEngine

from d2a import (
    D2A_CONFIG, AUTO_DETECTED_DB_TYPE, NAME_FORMATTER,
    declare, parse_models, parse_model, DB_TYPES,
    _extract_kwargs,
)
from d2a.resolvers import reverse_mapping
from d2a.template import TEMPLATE

REL_PARAMS = D2A_CONFIG.get("REL_PARAMS", {})
COL_PARAMS = D2A_CONFIG.get("COL_PARAMS", {})
TYPE_PARAMS = D2A_CONFIG.get("TYPE_PARAMS", {})
TYPES = D2A_CONFIG.get("TYPES", {})
BLOCKS = D2A_CONFIG.get("BLOCKS", {})


class Command(BaseCommand):
    help = "generates a file of sqlalchemy model definitions."

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, required=False, default="./models_sqla.py", help="generated file path")
        parser.add_argument("--template-path", type=str, required=False, help="template file path")
        parser.add_argument("--db-type", type=str, required=False, default=AUTO_DETECTED_DB_TYPE, help="db_type: Database type, for example `postgresql`. If omitted this option, it will be detected from django settings.")
        super().add_arguments(parser)

        return parser

    def handle(self, *args, **options):
        models = OrderedDict()
        for app in settings.INSTALLED_APPS:
            mods = app.split('.')
            for i in range(1, len(mods) + 1):
                mod = '.'.join(mods[:i])
                d = f'{mod}.models'
                try:
                    django_models = importlib.import_module(d)
                    for model in parse_models(django_models).values():
                        build_context(model, models, db_type=options["db_type"])
                except ImportError:
                    pass
        
        if options.get("template_path"):
            t = get_template(options["template_path"]).template
        else:
            t = Template(TEMPLATE)
        with open(options["path"], "w") as f:
            context = Context({
                "generated_at": timezone.now().strftime('%c %Z'),
                "command": " ".join(sys.argv),
                "models": models.values(),
                "blocks": BLOCKS,
            })
            f.write(t.render(context))


def build_context(django_model, models, db_type):
    model_info = parse_model(django_model)
    model_name = NAME_FORMATTER(django_model._meta.object_name)
    model_context = {
        "django_model": django_model,
        "table_name": model_info['table_name'],
        "model_name": model_name,
        "columns": OrderedDict(),
        "relationships": OrderedDict(),
    }

    rel_kwargs_map = OrderedDict()
    for name, kwargs in model_info['fields'].items():
        types = {t: kwargs.get(f'__{t}_type__', None) for t in DB_TYPES}
        type_kwargs = {t: kwargs.get(f'__{t}_type_kwargs__', {}) for t in DB_TYPES}
        type_key = 'default' if types.get(db_type) is None else db_type
        rel_kwargs = kwargs.get('__rel_kwargs__', {})
        if rel_kwargs:
            rel_kwargs_map[name] = rel_kwargs
        
        if not types[type_key]:
            continue

        field_type = TYPES.get("*") or TYPES.get(f"{model_name}.{name}") or reverse_mapping[types[type_key]]
        type_kwargs_extended = {**TYPE_PARAMS.get("*", {}), **TYPE_PARAMS.get(f"{model_name}.{name}", {})}
        type_args = render_args({**type_kwargs[type_key], **type_kwargs_extended})
        model_context["columns"][name] = [f"{field_type}({', '.join(type_args)})"]
        if '__fk_kwargs__' in kwargs:
            fk_args = render_args(kwargs['__fk_kwargs__'])
            model_context["columns"][name] += [f"ForeignKey({', '.join(fk_args)})"]
        
        kwargs_extended = {**COL_PARAMS.get("*", {}), **COL_PARAMS.get(f"{model_name}.{name}", {})}
        if "default" in kwargs:
            del kwargs["default"]
            logical_name = kwargs.get("__logical_name__")
            if "default" not in kwargs_extended and logical_name is not None:
                model_context["columns"][name] += [f"default=GET_DEFAULT('{django_model.__module__}.{model_name}.{logical_name}')"]

        model_context["columns"][name] += render_args({**kwargs, **kwargs_extended})

    for name, rel_kwargs in rel_kwargs_map.items():
        if '__logical_name__' in rel_kwargs:
            name = rel_kwargs['__logical_name__']
        
        rel_kwargs_extended = {**REL_PARAMS.get("*", {}), **REL_PARAMS.get(f"{model_name}.{name}", {})}
        model_context["relationships"][name] = [
            f"'{rel_kwargs['__related_model__']._meta.object_name}'",
            *render_args({**rel_kwargs, **rel_kwargs_extended}, rel_kwargs),
        ]
        if '__secondary_model__' in rel_kwargs:
            build_context(rel_kwargs['__secondary_model__'], models, db_type)

    models[model_name] = model_context


def render_args(kwargs: dict, context: dict={}):
    args = []
    for k, v in _extract_kwargs(kwargs).items():
        if isinstance(v, str):
            v = f'"{v}"'.format(**context)
        elif inspect.isclass(v) and issubclass(v, TypeEngine):
            v = reverse_mapping[v]
        args += [f"{k}={v}"]
    return args
