from sqlalchemy import types as default_types


class CIText(default_types.String):
    __visit_name__ = 'CITEXT'
