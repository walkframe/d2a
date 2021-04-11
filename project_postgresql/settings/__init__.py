from .base import *  # NOQA

from django.db.models import CharField, EmailField
from books.fields import CustomEmailField

D2A_CONFIG = {
    "REL_PARAMS": {
        "*": {
            "backref": "{__back__}",
        },
        "Book.category": {
            "lazy": "joined",
        },
    },
    "COL_PARAMS": {
        "*": {
            "doc": "testtest",
        },
    },
    "TYPE_PARAMS": {
        "*": {
        }
    },
    "MISSING": CharField,
    "ALIASES": {
        CustomEmailField: EmailField,
    },
}
