# coding: utf-8
import importlib
import types
import sys
from collections import OrderedDict

from django.conf import settings

from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .parsers import parse_models, parse_model

from .fields import alias, alias_dict, JSONType
from .db import (
    AUTO_DETECTED_DB_TYPE,
    query_expression, execute_expression,
    make_engine, make_session,
)
from .utils import get_camelcase

DB_TYPES = ['postgresql', 'mysql', 'oracle', 'sqlite3', 'firebird', 'mssql', 'default']


D2A_CONFIG = getattr(settings, 'D2A_CONFIG', {})
alias_dict(D2A_CONFIG.get('ALIASES', {}))
NAME_FORMATTER = D2A_CONFIG.get('NAME_FORMATTER', lambda name: get_camelcase(name, capitalize=True))

Base = declarative_base()
existing = {}


def _extract_kwargs(kwargs):
    return {k: v for k, v in kwargs.items() if not (k.startswith('__') and k.endswith('__'))}


def declare(django_model, db_type=AUTO_DETECTED_DB_TYPE, back_type='backref'):
    """It converts a django model to alchemy orm object.
    :param django.db.models.base.Model django_model: Django model object or equivalent object.
    :param str db_type: Database type, for example `postgresql`. If omitted this option, it will be detected from django settings.
    :param str back_type: Back relation type, `backref` or ``None`` (it does not support `back_populates`).
    This function is also called from `transfer` :)
    """

    model_info = parse_model(django_model)
    if django_model in existing:
        return existing[django_model]

    rel_options = OrderedDict()
    attrs = OrderedDict({'__tablename__': model_info['table_name']})
    for name, fields in model_info['fields'].items():
        rel_option = fields.get('__rel_kwargs__', {})
        if rel_option:
            rel_options[name] = rel_option

        col_types = {}
        col_type_options = {}
        for _db_type in DB_TYPES:
            col_types[_db_type] = fields.get('__{}_type__'.format(_db_type), None)
            col_type_options[_db_type] = fields.get('__{}_type_kwargs__'.format(_db_type), {})

        type_key = 'default' if col_types.get(db_type) is None else db_type
        if col_types[type_key]:
            col_args = [col_types[type_key](**col_type_options[type_key])]
            if '__fk_kwargs__' in fields:
                col_args.append(ForeignKey(**_extract_kwargs(fields['__fk_kwargs__'])))

            column = attrs[name] = Column(*col_args, **_extract_kwargs(fields))
            rel_option['foreign_keys'] = [column]

    for logical_name, rel_option in rel_options.items():
        if '__secondary_model__' in rel_option:
            secondary = rel_option['secondary'] = declare(rel_option['__secondary_model__'], db_type=db_type, back_type=back_type).__table__
        
        if '__logical_name__' in rel_option:
            logical_name = rel_option['__logical_name__']

        back = rel_option.get('__back__', None)
        if back and back_type:
            rel_option[back_type] = back.rstrip('+').lower()

        attrs[logical_name] = relationship(rel_option['__target__'], **_extract_kwargs(rel_option))

    cls = existing[django_model] = type(model_info['table_name'], (Base,), attrs)
    return cls


def transfer(models, exports, db_type=AUTO_DETECTED_DB_TYPE, back_type='backref', as_table=False, name_formatter=NAME_FORMATTER):
    """It makes sqlalchemy model objects from django models.

    :param module models: Django `models.py` or equivalent object.
    :param dict exports: Namespace which you want to put the models into. In most case, that is ``globals()``.
    :param str db_type: Database type, for example `postgresql`. If omitted this option, it will be detected from django settings.
    :param str back_type: Back relation type, `backref` or ``None`` (it does not support `back_populates`).
    :param bool as_table: Whether outputting as `SQL Expression` schema (``orm.__table__``) or not.
    :param function name_formatter: It receives an argument (model name) as ``str``, and returns formetted model name.
    """

    for model in parse_models(models).values():
        declare(model, db_type=db_type, back_type=back_type)

    for django_model, alchemy_model in existing.items():
        if models.__name__ == django_model.__module__:
            key = name_formatter(django_model._meta.object_name)
            exports[key] = alchemy_model.__table__ if as_table else alchemy_model


def autoload(config=D2A_CONFIG.get('AUTOLOAD', {})):
    """It loads all models automatically.
    """
    module = config.get('module', 'models_sqla')
    option = config.get('option', {})
    for app in settings.INSTALLED_APPS:
        mods = app.split('.')
        for i in range(1, len(mods) + 1):
            mod = '.'.join(mods[:i])
            d = '{mod}.models'.format(mod=mod)
            a = '{mod}.{module}'.format(mod=mod, module=module)
            if importlib.util.find_spec(d) is None:
                continue
            try:
                importlib.import_module(a)
            except ImportError:
                sys.modules[a] = types.ModuleType(a)
                transfer(importlib.import_module(d), sys.modules[a].__dict__, **option)


default_app_config = "d2a.apps.D2aConfig"
