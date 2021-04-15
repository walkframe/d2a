from .base import *

from django.db.models import CharField, EmailField
from books.fields import CustomEmailField

D2A_CONFIG = {
    "REL_PARAMS": {
        #"*": {
        #    "backref": "{__back__}",
        #},
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
        },
    },
    "TYPES": {
        "Book.title": "default_types.VARCHAR",
    },
    "BLOCKS": {
        "before_importing": "import os",
        "after_importing": "# import finished",
        "before_models": "# start defining models",
        "after_models": "# END OF FILE",
    },
    "MISSING": CharField,
    "ALIASES": {
        CustomEmailField: EmailField,
    },
    "AUTOLOAD": False,
}
