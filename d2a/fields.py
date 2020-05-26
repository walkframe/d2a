# coding: utf-8
import warnings

from django.db import models
from django.conf import settings
from django.contrib.postgres import fields as postgres_fields

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
        '_default_type': default_types.INTEGER,
        '_postgresql_type': postgresql_types.INTEGER,
        '_mysql_type': mysql_types.INTEGER,
        '_oracle_type': oracle_types.NUMBER,
        '_oracle_type_option': {'precision': 11},
        'autoincrement': True,
    },
    models.IntegerField: {
        '_default_type': default_types.INTEGER,
        '_postgresql_type': postgresql_types.INTEGER,
        '_oracle_type': oracle_types.NUMBER,
        '_mysql_type': mysql_types.INTEGER,
        '_oracle_type_option': {'precision': 11},
    },
    models.PositiveIntegerField: {
        '_default_type': default_types.INTEGER,
        '_postgresql_type': postgresql_types.INTEGER,
        '_mysql_type': mysql_types.INTEGER,
        '_oracle_type': oracle_types.NUMBER,
        '_mysql_type_option': {'unsigned': True},
        '_oracle_type_option': {'precision': 11},
    },
    models.SmallIntegerField: {
        '_default_type': default_types.SMALLINT,
        '_postgresql_type': postgresql_types.SMALLINT,
        '_mysql_type': mysql_types.SMALLINT,
        '_oracle_type': oracle_types.NUMBER,
        '_oracle_type_option': {'precision': 11},
    },
    models.PositiveSmallIntegerField: {
        '_default_type': default_types.SMALLINT,
        '_postgresql_type': postgresql_types.SMALLINT,
        '_mysql_type': mysql_types.SMALLINT,
        '_oracle_type': oracle_types.NUMBER,
        '_mysql_type_option': {'unsigned': True},
        '_oracle_type_option': {'precision': 11},
    },
    models.BigIntegerField: {
        '_default_type': default_types.BIGINT,
        '_postgresql_type': postgresql_types.BIGINT,
        '_mysql_type': mysql_types.BIGINT,
        '_oracle_type': oracle_types.NUMBER,
        '_oracle_type_option': {'precision': 19},
    },
    models.DecimalField: {
        '_default_type': default_types.DECIMAL,
        '_postgresql_type': postgresql_types.NUMERIC,
        '_mysql_type': mysql_types.NUMERIC,
        '_oracle_type': oracle_types.NUMBER,
        '_callback': lambda f: {
            '_default_type_option': {'precision': f.max_digits, 'scale': f.decimal_places},
            '_postgresql_type_option': {'precision': f.max_digits, 'scale': f.decimal_places},
            '_mysql_type_option': {'precision': f.max_digits, 'scale': f.decimal_places},
            '_oracle_type_option': {'precision': f.max_digits, 'scale': f.decimal_places},
        }
    },
    models.FloatField: {
        '_default_type': default_types.FLOAT,
        '_postgresql_type': postgresql_types.FLOAT,
        '_mysql_type': mysql_types.FLOAT,
        '_oracle_type': oracle_types.DOUBLE_PRECISION,
    },
    models.CharField: {
        '_default_type': default_types.VARCHAR,
        '_postgresql_type': postgresql_types.VARCHAR,
        '_mysql_type': mysql_types.VARCHAR,
        '_oracle_type': oracle_types.NVARCHAR2,
        '_callback': lambda f: {
            '_default_type_option': {'length': f.max_length},
            '_postgresql_type_option': {'length': f.max_length},
            '_mysql_type_option': {'length': f.max_length},
            '_oracle_type_option': {'length': f.max_length},
        },
    },
    models.SlugField: {
        '_default_type': default_types.VARCHAR,
        '_postgresql_type': postgresql_types.VARCHAR,
        '_mysql_type': mysql_types.VARCHAR,
        '_oracle_type': oracle_types.NVARCHAR2,
        '_callback': lambda f: {
            '_default_type_option': {'length': f.max_length},
            '_postgresql_type_option': {'length': f.max_length},
            '_mysql_type_option': {'length': f.max_length},
            '_oracle_type_option': {'length': f.max_length},
        },
    },
    models.URLField: {
        '_default_type': default_types.VARCHAR,
        '_postgresql_type': postgresql_types.VARCHAR,
        '_mysql_type': mysql_types.VARCHAR,
        '_oracle_type': oracle_types.VARCHAR2,
        '_callback': lambda f: {
            '_default_type_option': {'length': f.max_length},
            '_postgresql_type_option': {'length': f.max_length},
            '_mysql_type_option': {'length': f.max_length},
            '_oracle_type_option': {'length': f.max_length},
        },
    },
    models.EmailField: {
        '_default_type': default_types.VARCHAR,
        '_postgresql_type': postgresql_types.VARCHAR,
        '_mysql_type': mysql_types.VARCHAR,
        '_oracle_type': oracle_types.VARCHAR2,
        '_callback': lambda f: {
            '_default_type_option': {'length': f.max_length},
            '_postgresql_type_option': {'length': f.max_length},
            '_mysql_type_option': {'length': f.max_length},
            '_oracle_type_option': {'length': f.max_length},
        },
    },
    models.FileField: {
        '_default_type': default_types.VARCHAR,
        '_postgresql_type': postgresql_types.VARCHAR,
        '_mysql_type': mysql_types.VARCHAR,
        '_oracle_type': oracle_types.NVARCHAR2,
        '_callback': lambda f: {
            '_default_type_option': {'length': f.max_length},
            '_postgresql_type_option': {'length': f.max_length},
            '_mysql_type_option': {'length': f.max_length},
            '_oracle_type_option': {'length': f.max_length},
        },
    },
    models.FilePathField: {
        '_default_type': default_types.VARCHAR,
        '_postgresql_type': postgresql_types.VARCHAR,
        '_mysql_type': mysql_types.VARCHAR,
        '_oracle_type': oracle_types.NVARCHAR2,
        '_callback': lambda f: {
            '_default_type_option': {'length': f.max_length},
            '_postgresql_type_option': {'length': f.max_length},
            '_mysql_type_option': {'length': f.max_length},
            '_oracle_type_option': {'length': f.max_length},
        },
    },
    models.ImageField: {
        '_default_type': default_types.VARCHAR,
        '_postgresql_type': postgresql_types.VARCHAR,
        '_mysql_type': mysql_types.VARCHAR,
        '_oracle_type': oracle_types.NVARCHAR2,
        '_callback': lambda f: {
            '_default_type_option': {'length': f.max_length},
            '_postgresql_type_option': {'length': f.max_length},
            '_mysql_type_option': {'length': f.max_length},
            '_oracle_type_option': {'length': f.max_length},
        },
    },
    models.IPAddressField: {
        '_default_type': default_types.CHAR,
        '_postgresql_type': postgresql_types.INET,
        '_mysql_type': mysql_types.CHAR,
        '_oracle_type': oracle_types.VARCHAR2,
        '_default_type_option': {'length': 15},
        '_mysql_type_option': {'length': 15},
        '_oracle_type_option': {'length': 15},
    },
    models.GenericIPAddressField: {
        '_default_type': default_types.CHAR,
        '_postgresql_type': postgresql_types.INET,
        '_mysql_type': mysql_types.CHAR,
        '_oracle_type': oracle_types.VARCHAR2,
        '_default_type_option': {'length': 39},
        '_mysql_type_option': {'length': 39},
        '_oracle_type_option': {'length': 39},
    },
    models.BinaryField: {
        '_default_type': default_types.BINARY,
        '_postgresql_type': postgresql_types.BYTEA,
        '_mysql_type': mysql_types.LONGBLOB,
        '_oracle_type': oracle_types.BLOB,
    },
    models.DurationField: {
        '_default_type': default_types.BIGINT,
        '_postgresql_type': postgresql_types.INTERVAL,
        '_mysql_type': mysql_types.BIGINT,
        '_oracle_type': oracle_types.INTERVAL,
        '_oracle_type_option': {'day_precision': 9, 'second_precision': 6}
    },
    models.UUIDField: {
        '_default_type': default_types.CHAR,
        '_postgresql_type': postgresql_types.UUID,
        '_mysql_type': mysql_types.CHAR,
        '_oracle_type': oracle_types.VARCHAR2,
        '_default_type_option': {'length': 32},
        '_mysql_type_option': {'length': 32},
        '_oracle_type_option': {'length': 32},
    },
    models.TextField: {
        '_default_type': default_types.TEXT,
        '_postgresql_type': postgresql_types.TEXT,
        '_mysql_type': mysql_types.LONGTEXT,
        '_oracle_type': oracle_types.NCLOB,
    },
    models.DateTimeField: {
        '_default_type': default_types.DATETIME,
        '_postgresql_type': postgresql_types.TIMESTAMP,
        '_mysql_type': mysql_types.DATETIME,
        '_oracle_type': oracle_types.TIMESTAMP,
    },
    models.DateField: {
        '_default_type': default_types.DATE,
        '_postgresql_type': postgresql_types.DATE,
        '_mysql_type': mysql_types.DATE,
        '_oracle_type': oracle_types.DATE,
    },
    models.TimeField: {
        '_default_type': default_types.TIME,
        '_postgresql_type': postgresql_types.TIME,
        '_mysql_type': mysql_types.TIME,
        '_oracle_type': oracle_types.TIMESTAMP,
    },
    models.BooleanField: {
        '_default_type': default_types.BOOLEAN,
        '_postgresql_type': postgresql_types.BOOLEAN,
        '_mysql_type': mysql_types.BOOLEAN,
        '_oracle_type': oracle_types.NUMBER,
        '_oracle_type_option': {'precision': 1},
    },
    models.NullBooleanField: {
        '_default_type': default_types.BOOLEAN,
        '_postgresql_type': postgresql_types.BOOLEAN,
        '_mysql_type': mysql_types.BOOLEAN,
        '_oracle_type': oracle_types.NUMBER,
        '_oracle_type_option': {'precision': 1},
        'nullable': True,
    },
    models.ForeignKey: {
        '_callback': lambda f: {
            '_callback': lambda f: (mapping[type(f.target_field)], f.target_field),
            '_rel_option': {
                '_logical_name': f.name,
                '_back': f.related_query_name(),
                '_target': f.related_model()._meta.db_table,
            },
            '_fk_option': {
                'column': '{meta.db_table}.{meta.pk.attname}'.format(meta=f.related_model._meta),
                'ondelete': f.remote_field.on_delete.__name__,
            },
        },
    },
    models.OneToOneField: {
        '_callback': lambda f: {
            '_callback': lambda f: (mapping[type(f.target_field)], f.target_field),
            '_rel_option': {
                '_logical_name': f.name,
                '_back': f.related_query_name(),
                '_target': f.related_model()._meta.db_table,
                'uselist': False,
            },
            '_fk_option': {
                'column': '{meta.db_table}.{meta.pk.attname}'.format(meta=f.related_model._meta),
                'ondelete': f.remote_field.on_delete.__name__,
            },
        },
    },
    M2MField: {
        '_callback': lambda f: {
            '_rel_option': {
                '_secondary_model': f.rel.through,
                '_target_field': f.field.m2m_target_field_name(),
                '_remote_primary_field': f.field.m2m_column_name(),
                '_remote_secondary_field': f.field.m2m_reverse_name(),
                '_back': f.field.related_query_name(),
                '_target': f.rel.model._meta.db_table,
            },
        } if not f.reverse else {}
    },
}

try:
    # deprecated
    mapping[models.CommaSeparatedIntegerField] = {
        '_default_type': default_types.VARCHAR,
        '_postgresql_type': postgresql_types.VARCHAR,
        '_mysql_type': mysql_types.VARCHAR,
        '_oracle_type': oracle_types.VARCHAR2,
        '_callback': lambda f: {
            '_default_type_option': {'length': f.max_length},
            '_postgresql_type_option': {'length': f.max_length},
            '_mysql_type_option': {'length': f.max_length},
            '_oracle_type_option': {'length': f.max_length},
        }
    }
except AttributeError:
    pass


try:
    mapping[models.PositiveBigIntegerField] = {
        '_default_type': default_types.BIGINT,
        '_postgresql_type': postgresql_types.BIGINT,
        '_mysql_type': mysql_types.BIGINT,
        '_oracle_type': oracle_types.NUMBER,
        '_mysql_type_option': {'unsigned': True},
        '_oracle_type_option': {'precision': 19},
    }
except AttributeError:
    pass

try:
    # 1.10 or later supports
    mapping[models.BigAutoField] = {
        '_default_type': default_types.BIGINT,
        '_postgresql_type': postgresql_types.BIGINT,
        '_mysql_type': mysql_types.BIGINT,
        '_oracle_type': oracle_types.NUMBER,
        '_oracle_type_option': {'precision': 19},
        'autoincrement': True,
    }
except AttributeError:
    pass

try:
    # 3.0 or later supports
    mapping[models.SmallAutoField] = {
        '_default_type': default_types.SMALLINT,
        '_postgresql_type': postgresql_types.SMALLINT,
        '_mysql_type': mysql_types.SMALLINT,
        '_oracle_type': oracle_types.NUMBER,
        '_oracle_type_option': {'precision': 5},
        'autoincrement': True,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.ArrayField] = {
        '_default_type': postgresql_types.ARRAY,
        '_postgresql_type': postgresql_types.ARRAY,
        '_mysql_type': default_types.ARRAY,
        '_oracle_type': default_types.ARRAY,
        '_callback': lambda f: {
            '_default_type_option': {'item_type': mapping[type(f.base_field)]['_default_type']},
            '_postgresql_type_option': {'item_type': mapping[type(f.base_field)].get('_postgresql_type') or mapping[type(f.base_field)]['_default_type']},
        },
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.HStoreField] = {
        '_default_type': postgresql_types.HSTORE,
        '_postgresql_type': postgresql_types.HSTORE,
    }
except AttributeError:
    pass


# Never matched. For alias of 3rd-party.
JSONType, JSONRule = 'JSONType', {
    '_default_type': default_types.JSON,
    '_postgresql_type': postgresql_types.JSON,
    '_mysql_type': mysql_types.JSON,
    '_oracle_type': default_types.JSON,
}

mapping[JSONType] = JSONRule

try:
    mapping[postgres_fields.JSONField] = {
        **JSONRule,
        '_default_type': postgresql_types.JSONB,
        '_postgresql_type': postgresql_types.JSONB,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.CICharField] = {
        '_default_type': CIText,
        '_postgresql_type': CIText,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.CIEmailField] = {
        '_default_type': CIText,
        '_postgresql_type': CIText,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.CITextField] = {
        '_default_type': CIText,
        '_postgresql_type': CIText,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.IntegerRangeField] = {
        '_default_type': postgresql_types.INT4RANGE,
        '_postgresql_type': postgresql_types.INT4RANGE,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.BigIntegerRangeField] = {
        '_default_type': postgresql_types.INT8RANGE,
        '_postgresql_type': postgresql_types.INT8RANGE,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.DecimalRangeField] = {
        '_default_type': postgresql_types.NUMRANGE,
        '_postgresql_type': postgresql_types.NUMRANGE,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.FloatRangeField] = {
        '_default_type': postgresql_types.NUMRANGE,
        '_postgresql_type': postgresql_types.NUMRANGE,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.DateTimeRangeField] = {
        '_default_type': postgresql_types.TSTZRANGE if settings.USE_TZ else postgresql_types.TSRANGE,
        '_postgresql_type': postgresql_types.TSTZRANGE if settings.USE_TZ else postgresql_types.TSRANGE,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.DateRangeField] = {
        '_default_type': postgresql_types.DATERANGE,
        '_postgresql_type': postgresql_types.DATERANGE,
    }
except AttributeError:
    pass

try:
    from .geoalchemy2 import geo_mapping
    mapping.update(geo_mapping)

except (ImportError, AttributeError) as e:
    if D2A_CONFIG.get('USE_GEOALCHEMY2', False):
        warnings.warn('An error occured: {}. HINT: GeoAlchemy2 should be installed when you use GeoDjango.'.format(e))
