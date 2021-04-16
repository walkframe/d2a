# coding: utf-8
import logging
import warnings
from collections import OrderedDict


from django.db.models.base import ModelBase
from django.db.models.fields import NOT_PROVIDED
from django.db import models

from .fields import mapping
from .compat import M2MField
from .missing import fallback

logger = logging.getLogger(__name__)


def get_m2m_fields(model):
    return {
        k: v for k, v in vars(model).items()
        if isinstance(v, M2MField)
    }


def parse_field(field):
    info = {}
    field_type = type(field)

    for django_attr, alchemy_attr in [
        ('primary_key', 'primary_key'), 
        ('unique', 'unique'), 
        ('null', 'nullable'),
    ]:
        if hasattr(field, django_attr):
            info[alchemy_attr] = getattr(field, django_attr)

    if getattr(field, 'default', NOT_PROVIDED) is not NOT_PROVIDED:
        info['default'] = field.default

    try:
        conf = mapping[field_type]
    except KeyError as e:
        alt = fallback(field, e)
        conf = mapping.get(alt, {})
    
    info.update(conf)
    while '__callback__' in info:
        result = info.pop('__callback__')(field)
        if isinstance(result, tuple):
            result, field = result
        info.update(result)
    return info


def parse_model(model, callback=parse_field):
    info = {'table_name': model._meta.db_table, 'fields': OrderedDict()}
    for field in model._meta.fields:
        info['fields'][field.column] = callback(field)
        info['fields'][field.column]["__logical_name__"] = field.name

    for name, field in get_m2m_fields(model).items():
        try:
            info['fields'][name] = callback(field)
        except AttributeError as e:
            # it raises an attribute exception when AUTH_USER_MODEL is changed.
            from django.contrib.auth import get_user_model, models as auth_models
            if get_user_model() is auth_models.User:
                logger.warning('An intermediate table (refs %(table_name)) was not created.', info)
            break
    return info


def parse_models(module):
    models = {}
    for name, model in [(name, getattr(module, name)) for name in dir(module)]:
        if isinstance(model, ModelBase) and not model._meta.abstract:
            models[name] = model
    return models
