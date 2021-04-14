from .base import *  # NOQA

from django.db.models import CharField, EmailField
from books.fields import CustomEmailField

D2A_CONFIG = {
    "MISSING": CharField,
    "ALIASES": {
        CustomEmailField: EmailField,
    },
}