from sqlalchemy import types as default_types
from sqlalchemy.dialects import (
    postgresql as postgresql_types,
    mysql as mysql_types,
    oracle as oracle_types,
)
from . import original_types

try:
    from geoalchemy2 import types as geotypes
except ImportError:
    pass

alchemy_fields = [
    "default_types.INTEGER",
    "postgresql_types.INTEGER",
    "mysql_types.INTEGER",
    "oracle_types.NUMBER",
    "default_types.SMALLINT",
    "postgresql_types.SMALLINT",
    "mysql_types.SMALLINT",
    "oracle_types.NUMBER",
    "default_types.BIGINT",
    "postgresql_types.BIGINT",
    "mysql_types.BIGINT",
    "oracle_types.NUMBER",
    "default_types.DECIMAL",
    "postgresql_types.NUMERIC",
    "mysql_types.NUMERIC",
    "oracle_types.NUMBER",
    "default_types.FLOAT",
    "postgresql_types.FLOAT",
    "mysql_types.FLOAT",
    "oracle_types.DOUBLE_PRECISION",
    "default_types.VARCHAR",
    "postgresql_types.VARCHAR",
    "mysql_types.VARCHAR",
    "oracle_types.NVARCHAR2",
    "default_types.CHAR",
    "postgresql_types.INET",
    "mysql_types.CHAR",
    "default_types.BINARY",
    "postgresql_types.BYTEA",
    "mysql_types.LONGBLOB",
    "oracle_types.BLOB",
    "oracle_types.INTERVAL",
    "postgresql_types.INTERVAL",
    "postgresql_types.UUID",
    "default_types.TEXT",
    "postgresql_types.TEXT",
    "mysql_types.LONGTEXT",
    "oracle_types.NCLOB",
    "default_types.DATETIME",
    "postgresql_types.TIMESTAMP",
    "mysql_types.DATETIME",
    "oracle_types.TIMESTAMP",
    "default_types.DATE",
    "postgresql_types.DATE",
    "mysql_types.DATE",
    "oracle_types.DATE",
    "default_types.TIME",
    "postgresql_types.TIME",
    "mysql_types.TIME",
    "oracle_types.TIMESTAMP",
    "default_types.BOOLEAN",
    "postgresql_types.BOOLEAN",
    "mysql_types.BOOLEAN",
    "oracle_types.NUMBER",
    "postgresql_types.ARRAY",
    "default_types.ARRAY",
    "postgresql_types.HSTORE",
    "default_types.JSON",
    "postgresql_types.JSON",
    "mysql_types.JSON",
    "postgresql_types.JSONB",
    
    "postgresql_types.INT4RANGE",
    "postgresql_types.INT8RANGE",
    "postgresql_types.NUMRANGE",
    "postgresql_types.TSTZRANGE",
    "postgresql_types.DATERANGE",
    "geotypes.Geography",
    "geotypes.Geometry",
    "geotypes.Raster",

    "original_types.CIText",
]

forward_mapping = {}
reverse_mapping = {}

for code in alchemy_fields:
    try:
        entity = eval(code)
    except (NameError, AttributeError):
        continue

    forward_mapping[code] = entity
    reverse_mapping[entity] = code

