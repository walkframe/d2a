# coding: utf-8
import warnings

from django.db import models
from django.conf import settings
from django.contrib.postgres import fields as postgres_fields
from django.core.exceptions import ImproperlyConfigured

from sqlalchemy import types as default_types
from sqlalchemy.dialects import (
    postgresql as postgresql_types,
    mysql as mysql_types,
    oracle as oracle_types,
)

from .compat import M2MField
from .original_types import CIText

"""
Mapping definition

:postgresql:

  - https://github.com/django/django/blob/master/django/db/backends/postgresql/base.py
  - https://github.com/sqlalchemy/sqlalchemy/blob/master/lib/sqlalchemy/dialects/postgresql/__init__.py

  - https://github.com/django/django/blob/master/django/contrib/gis/db/models/fields.py
  - https://github.com/geoalchemy/geoalchemy2/blob/master/geoalchemy2/types.py

:mysql:

  - https://github.com/django/django/blob/master/django/db/backends/mysql/base.py
  - https://github.com/sqlalchemy/sqlalchemy/blob/master/lib/sqlalchemy/dialects/mysql/__init__.py

:oracle:

  - https://github.com/django/django/blob/master/django/db/backends/oracle/base.py
  - https://github.com/sqlalchemy/sqlalchemy/blob/master/lib/sqlalchemy/dialects/oracle/__init__.py

"""


def alias(new_field, existing_field):
    """It defines a new converting rule same with existing one.

    :param django.db.models.fields.Field new_field: A field which you want to add.
    :param django.db.models.fields.Field existing_field: A field copied from.
    """
    mapping[new_field] = mapping[existing_field]


def alias_dict(extra_mapping={}):
    for new_field, existing_field in extra_mapping.items():
        alias(new_field, existing_field)


D2A_CONFIG = getattr(settings, 'D2A_CONFIG', {})

mapping = {
    models.AutoField: {
        '__default_type__': default_types.INTEGER,
        '__postgresql_type__': postgresql_types.INTEGER,
        '__mysql_type__': mysql_types.INTEGER,
        '__oracle_type__': oracle_types.NUMBER,
        '__oracle_type_kwargs__': {'precision': 11},
        'autoincrement': True,
    },
    models.IntegerField: {
        '__default_type__': default_types.INTEGER,
        '__postgresql_type__': postgresql_types.INTEGER,
        '__oracle_type__': oracle_types.NUMBER,
        '__mysql_type__': mysql_types.INTEGER,
        '__oracle_type_kwargs__': {'precision': 11},
    },
    models.PositiveIntegerField: {
        '__default_type__': default_types.INTEGER,
        '__postgresql_type__': postgresql_types.INTEGER,
        '__mysql_type__': mysql_types.INTEGER,
        '__oracle_type__': oracle_types.NUMBER,
        '__mysql_type_kwargs__': {'unsigned': True},
        '__oracle_type_kwargs__': {'precision': 11},
    },
    models.SmallIntegerField: {
        '__default_type__': default_types.SMALLINT,
        '__postgresql_type__': postgresql_types.SMALLINT,
        '__mysql_type__': mysql_types.SMALLINT,
        '__oracle_type__': oracle_types.NUMBER,
        '__oracle_type_kwargs__': {'precision': 11},
    },
    models.PositiveSmallIntegerField: {
        '__default_type__': default_types.SMALLINT,
        '__postgresql_type__': postgresql_types.SMALLINT,
        '__mysql_type__': mysql_types.SMALLINT,
        '__oracle_type__': oracle_types.NUMBER,
        '__mysql_type_kwargs__': {'unsigned': True},
        '__oracle_type_kwargs__': {'precision': 11},
    },
    models.BigIntegerField: {
        '__default_type__': default_types.BIGINT,
        '__postgresql_type__': postgresql_types.BIGINT,
        '__mysql_type__': mysql_types.BIGINT,
        '__oracle_type__': oracle_types.NUMBER,
        '__oracle_type_kwargs__': {'precision': 19},
    },
    models.DecimalField: {
        '__default_type__': default_types.DECIMAL,
        '__postgresql_type__': postgresql_types.NUMERIC,
        '__mysql_type__': mysql_types.NUMERIC,
        '__oracle_type__': oracle_types.NUMBER,
        '__callback__': lambda f: {
            '__default_type_kwargs__': {'precision': f.max_digits, 'scale': f.decimal_places},
            '__postgresql_type_kwargs__': {'precision': f.max_digits, 'scale': f.decimal_places},
            '__mysql_type_kwargs__': {'precision': f.max_digits, 'scale': f.decimal_places},
            '__oracle_type_kwargs__': {'precision': f.max_digits, 'scale': f.decimal_places},
        }
    },
    models.FloatField: {
        '__default_type__': default_types.FLOAT,
        '__postgresql_type__': postgresql_types.FLOAT,
        '__mysql_type__': mysql_types.FLOAT,
        '__oracle_type__': oracle_types.DOUBLE_PRECISION,
    },
    models.CharField: {
        '__default_type__': default_types.VARCHAR,
        '__postgresql_type__': postgresql_types.VARCHAR,
        '__mysql_type__': mysql_types.VARCHAR,
        '__oracle_type__': oracle_types.NVARCHAR2,
        '__callback__': lambda f: {
            '__default_type_kwargs__': {'length': f.max_length},
            '__postgresql_type_kwargs__': {'length': f.max_length},
            '__mysql_type_kwargs__': {'length': f.max_length},
            '__oracle_type_kwargs__': {'length': f.max_length},
        },
    },
    models.SlugField: {
        '__default_type__': default_types.VARCHAR,
        '__postgresql_type__': postgresql_types.VARCHAR,
        '__mysql_type__': mysql_types.VARCHAR,
        '__oracle_type__': oracle_types.NVARCHAR2,
        '__callback__': lambda f: {
            '__default_type_kwargs__': {'length': f.max_length},
            '__postgresql_type_kwargs__': {'length': f.max_length},
            '__mysql_type_kwargs__': {'length': f.max_length},
            '__oracle_type_kwargs__': {'length': f.max_length},
        },
    },
    models.URLField: {
        '__default_type__': default_types.VARCHAR,
        '__postgresql_type__': postgresql_types.VARCHAR,
        '__mysql_type__': mysql_types.VARCHAR,
        '__oracle_type__': oracle_types.VARCHAR2,
        '__callback__': lambda f: {
            '__default_type_kwargs__': {'length': f.max_length},
            '__postgresql_type_kwargs__': {'length': f.max_length},
            '__mysql_type_kwargs__': {'length': f.max_length},
            '__oracle_type_kwargs__': {'length': f.max_length},
        },
    },
    models.EmailField: {
        '__default_type__': default_types.VARCHAR,
        '__postgresql_type__': postgresql_types.VARCHAR,
        '__mysql_type__': mysql_types.VARCHAR,
        '__oracle_type__': oracle_types.VARCHAR2,
        '__callback__': lambda f: {
            '__default_type_kwargs__': {'length': f.max_length},
            '__postgresql_type_kwargs__': {'length': f.max_length},
            '__mysql_type_kwargs__': {'length': f.max_length},
            '__oracle_type_kwargs__': {'length': f.max_length},
        },
    },
    models.FileField: {
        '__default_type__': default_types.VARCHAR,
        '__postgresql_type__': postgresql_types.VARCHAR,
        '__mysql_type__': mysql_types.VARCHAR,
        '__oracle_type__': oracle_types.NVARCHAR2,
        '__callback__': lambda f: {
            '__default_type_kwargs__': {'length': f.max_length},
            '__postgresql_type_kwargs__': {'length': f.max_length},
            '__mysql_type_kwargs__': {'length': f.max_length},
            '__oracle_type_kwargs__': {'length': f.max_length},
        },
    },
    models.FilePathField: {
        '__default_type__': default_types.VARCHAR,
        '__postgresql_type__': postgresql_types.VARCHAR,
        '__mysql_type__': mysql_types.VARCHAR,
        '__oracle_type__': oracle_types.NVARCHAR2,
        '__callback__': lambda f: {
            '__default_type_kwargs__': {'length': f.max_length},
            '__postgresql_type_kwargs__': {'length': f.max_length},
            '__mysql_type_kwargs__': {'length': f.max_length},
            '__oracle_type_kwargs__': {'length': f.max_length},
        },
    },
    models.ImageField: {
        '__default_type__': default_types.VARCHAR,
        '__postgresql_type__': postgresql_types.VARCHAR,
        '__mysql_type__': mysql_types.VARCHAR,
        '__oracle_type__': oracle_types.NVARCHAR2,
        '__callback__': lambda f: {
            '__default_type_kwargs__': {'length': f.max_length},
            '__postgresql_type_kwargs__': {'length': f.max_length},
            '__mysql_type_kwargs__': {'length': f.max_length},
            '__oracle_type_kwargs__': {'length': f.max_length},
        },
    },
    models.IPAddressField: {
        '__default_type__': default_types.CHAR,
        '__postgresql_type__': postgresql_types.INET,
        '__mysql_type__': mysql_types.CHAR,
        '__oracle_type__': oracle_types.VARCHAR2,
        '__default_type_kwargs__': {'length': 15},
        '__mysql_type_kwargs__': {'length': 15},
        '__oracle_type_kwargs__': {'length': 15},
    },
    models.GenericIPAddressField: {
        '__default_type__': default_types.CHAR,
        '__postgresql_type__': postgresql_types.INET,
        '__mysql_type__': mysql_types.CHAR,
        '__oracle_type__': oracle_types.VARCHAR2,
        '__default_type_kwargs__': {'length': 39},
        '__mysql_type_kwargs__': {'length': 39},
        '__oracle_type_kwargs__': {'length': 39},
    },
    models.BinaryField: {
        '__default_type__': default_types.BINARY,
        '__postgresql_type__': postgresql_types.BYTEA,
        '__mysql_type__': mysql_types.LONGBLOB,
        '__oracle_type__': oracle_types.BLOB,
    },
    models.DurationField: {
        '__default_type__': default_types.BIGINT,
        '__postgresql_type__': postgresql_types.INTERVAL,
        '__mysql_type__': mysql_types.BIGINT,
        '__oracle_type__': oracle_types.INTERVAL,
        '__oracle_type_kwargs__': {'day_precision': 9, 'second_precision': 6}
    },
    models.UUIDField: {
        '__default_type__': default_types.CHAR,
        '__postgresql_type__': postgresql_types.UUID,
        '__mysql_type__': mysql_types.CHAR,
        '__oracle_type__': oracle_types.VARCHAR2,
        '__default_type_kwargs__': {'length': 32},
        '__mysql_type_kwargs__': {'length': 32},
        '__oracle_type_kwargs__': {'length': 32},
    },
    models.TextField: {
        '__default_type__': default_types.TEXT,
        '__postgresql_type__': postgresql_types.TEXT,
        '__mysql_type__': mysql_types.LONGTEXT,
        '__oracle_type__': oracle_types.NCLOB,
    },
    models.DateTimeField: {
        '__default_type__': default_types.DATETIME,
        '__postgresql_type__': postgresql_types.TIMESTAMP,
        '__mysql_type__': mysql_types.DATETIME,
        '__oracle_type__': oracle_types.TIMESTAMP,
    },
    models.DateField: {
        '__default_type__': default_types.DATE,
        '__postgresql_type__': postgresql_types.DATE,
        '__mysql_type__': mysql_types.DATE,
        '__oracle_type__': oracle_types.DATE,
    },
    models.TimeField: {
        '__default_type__': default_types.TIME,
        '__postgresql_type__': postgresql_types.TIME,
        '__mysql_type__': mysql_types.TIME,
        '__oracle_type__': oracle_types.TIMESTAMP,
    },
    models.BooleanField: {
        '__default_type__': default_types.BOOLEAN,
        '__postgresql_type__': postgresql_types.BOOLEAN,
        '__mysql_type__': mysql_types.BOOLEAN,
        '__oracle_type__': oracle_types.NUMBER,
        '__oracle_type_kwargs__': {'precision': 1},
    },
    models.ForeignKey: {
        '__callback__': lambda f: {
            '__callback__': lambda f: (mapping[type(f.target_field)], f.target_field),
            '__rel_kwargs__': {
                '__logical_name__': f.name,
                '__back__': f.related_query_name().rstrip('+').lower(),
                '__back_target__': f.model._meta.db_table,
                '__target__': f.related_model._meta.db_table,
                '__model__': f.model,
                '__related_model__': f.related_model,
                'foreign_keys': f"[{f.model._meta.db_table}.c.{f.column}]",
                'remote_side': f"[{f.model._meta.db_table}.c.{f.target_field.column}]" if f.model == f.related_model else None,
            },
            '__fk_kwargs__': {
                'column': '{meta.db_table}.{meta.pk.column}'.format(meta=f.related_model._meta),
                'ondelete': f.remote_field.on_delete.__name__,
            },
        },
    },
    models.OneToOneField: {
        '__callback__': lambda f: {
            '__callback__': lambda f: (mapping[type(f.target_field)], f.target_field),
            '__rel_kwargs__': {
                '__logical_name__': f.name,
                '__back__': f.related_query_name().rstrip('+').lower(),
                '__back_target__': f.model._meta.db_table,
                '__target__': f.related_model._meta.db_table,
                '__model__': f.model,
                '__related_model__': f.related_model,
                'foreign_keys': f"[{f.model._meta.db_table}.c.{f.column}]",
                'remote_side': f"[{f.model._meta.db_table}.c.{f.target_field.column}]" if f.model == f.related_model else None,
                'uselist': False,
            },
            '__fk_kwargs__': {
                'column': '{meta.db_table}.{meta.pk.column}'.format(meta=f.related_model._meta),
                'ondelete': f.remote_field.on_delete.__name__,
            },
        },
    },
    M2MField: {
        '__callback__': lambda f: {
            '__rel_kwargs__': {
                '__secondary_model__': f.rel.through,
                '__target_field__': f.field.m2m_target_field_name(),
                '__remote_primary_field__': f.field.m2m_column_name(),
                '__remote_secondary_field__': f.field.m2m_reverse_name(),
                '__back__': f.field.related_query_name().rstrip('+').lower(),
                '__back_target__': f.rel.related_model._meta.db_table,
                '__target__': f.rel.model._meta.db_table,
                '__model__': f.rel.related_model,
                '__related_model__': f.rel.model,
                'secondary': f.rel.through._meta.db_table,
                'foreign_keys': (
                    f"[{f.rel.through._meta.db_table}.c.{f.rel.field._m2m_column_cache}]"
                    if f.field.model == f.field.related_model else
                    f"[{f.rel.through._meta.db_table}.c.{f.rel.field._m2m_column_cache}, {f.rel.through._meta.db_table}.c.{f.rel.field._m2m_reverse_column_cache}]"
                ),
                'remote_side': f"[{f.field.model._meta.db_table}.c.{f.rel.target_field.column}]" if f.field.model == f.field.related_model else None,
            },
        } if not f.reverse else {}
    },
}

try:
    # Deprecated since version 3.1
    mapping[models.NullBooleanField] = {
        '__default_type__': default_types.BOOLEAN,
        '__postgresql_type__': postgresql_types.BOOLEAN,
        '__mysql_type__': mysql_types.BOOLEAN,
        '__oracle_type__': oracle_types.NUMBER,
        '__oracle_type_kwargs__': {'precision': 1},
        'nullable': True,
    }
except AttributeError:
    pass

try:
    # deprecated
    mapping[models.CommaSeparatedIntegerField] = {
        '__default_type__': default_types.VARCHAR,
        '__postgresql_type__': postgresql_types.VARCHAR,
        '__mysql_type__': mysql_types.VARCHAR,
        '__oracle_type__': oracle_types.VARCHAR2,
        '__callback__': lambda f: {
            '__default_type_kwargs__': {'length': f.max_length},
            '__postgresql_type_kwargs__': {'length': f.max_length},
            '__mysql_type_kwargs__': {'length': f.max_length},
            '__oracle_type_kwargs__': {'length': f.max_length},
        }
    }
except AttributeError:
    pass

try:
    mapping[models.PositiveBigIntegerField] = {
        '__default_type__': default_types.BIGINT,
        '__postgresql_type__': postgresql_types.BIGINT,
        '__mysql_type__': mysql_types.BIGINT,
        '__oracle_type__': oracle_types.NUMBER,
        '__mysql_type_kwargs__': {'unsigned': True},
        '__oracle_type_kwargs__': {'precision': 19},
    }
except AttributeError:
    pass

try:
    # 1.10 or later supports
    mapping[models.BigAutoField] = {
        '__default_type__': default_types.BIGINT,
        '__postgresql_type__': postgresql_types.BIGINT,
        '__mysql_type__': mysql_types.BIGINT,
        '__oracle_type__': oracle_types.NUMBER,
        '__oracle_type_kwargs__': {'precision': 19},
        'autoincrement': True,
    }
except AttributeError:
    pass

try:
    # 3.0 or later supports
    mapping[models.SmallAutoField] = {
        '__default_type__': default_types.SMALLINT,
        '__postgresql_type__': postgresql_types.SMALLINT,
        '__mysql_type__': mysql_types.SMALLINT,
        '__oracle_type__': oracle_types.NUMBER,
        '__oracle_type_kwargs__': {'precision': 5},
        'autoincrement': True,
    }
except AttributeError:
    pass

try:
    def _parse_array(field, db_type):
        dimensions = 1
        while isinstance(field, postgres_fields.ArrayField):
            field = field.base_field
            dimensions += 1
        return {"item_type": mapping[type(field)].get(f"__{db_type}_type__"), "dimensions": dimensions}

    mapping[postgres_fields.ArrayField] = {
        '__default_type__': postgresql_types.ARRAY,
        '__postgresql_type__': postgresql_types.ARRAY,
        '__mysql_type__': default_types.ARRAY,
        '__oracle_type__': default_types.ARRAY,
        '__callback__': lambda f: {
            '__default_type_kwargs__': _parse_array(f.base_field, "default"),
            '__postgresql_type_kwargs__': _parse_array(f.base_field, "postgresql"),
        },
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.HStoreField] = {
        '__default_type__': postgresql_types.HSTORE,
        '__postgresql_type__': postgresql_types.HSTORE,
    }
except AttributeError:
    pass


# Never matched. For alias of 3rd-party.
JSONType, JSONRule = 'JSONType', {
    '__default_type__': default_types.JSON,
    '__postgresql_type__': postgresql_types.JSON,
    '__mysql_type__': mysql_types.JSON,
    '__oracle_type__': default_types.JSON,
}

mapping[JSONType] = JSONRule

try:
    mapping[models.JSONField] = {
        **JSONRule,
        '__postgresql_type__': postgresql_types.JSONB,
        '__oracle_type__': oracle_types.NCLOB,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.JSONField] = {
        **JSONRule,
        '__default_type__': postgresql_types.JSONB,
        '__postgresql_type__': postgresql_types.JSONB,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.CICharField] = {
        '__default_type__': CIText,
        '__postgresql_type__': CIText,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.CIEmailField] = {
        '__default_type__': CIText,
        '__postgresql_type__': CIText,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.CITextField] = {
        '__default_type__': CIText,
        '__postgresql_type__': CIText,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.IntegerRangeField] = {
        '__default_type__': postgresql_types.INT4RANGE,
        '__postgresql_type__': postgresql_types.INT4RANGE,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.BigIntegerRangeField] = {
        '__default_type__': postgresql_types.INT8RANGE,
        '__postgresql_type__': postgresql_types.INT8RANGE,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.DecimalRangeField] = {
        '__default_type__': postgresql_types.NUMRANGE,
        '__postgresql_type__': postgresql_types.NUMRANGE,
    }
except AttributeError:
    pass

try:
    # deprecated
    mapping[postgres_fields.FloatRangeField] = {
        '__default_type__': postgresql_types.NUMRANGE,
        '__postgresql_type__': postgresql_types.NUMRANGE,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.DateTimeRangeField] = {
        '__default_type__': postgresql_types.TSTZRANGE if settings.USE_TZ else postgresql_types.TSRANGE,
        '__postgresql_type__': postgresql_types.TSTZRANGE if settings.USE_TZ else postgresql_types.TSRANGE,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.DateRangeField] = {
        '__default_type__': postgresql_types.DATERANGE,
        '__postgresql_type__': postgresql_types.DATERANGE,
    }
except AttributeError:
    pass

try:
    from .geoalchemy2 import geo_mapping
    mapping.update(geo_mapping)

except (ImportError, AttributeError, ImproperlyConfigured) as e:
    if D2A_CONFIG.get('USE_GEOALCHEMY2', False):
        warnings.warn('An error occured: {}. HINT: GeoAlchemy2 should be installed when you use GeoDjango.'.format(e))
