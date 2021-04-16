import warnings

from django.conf import settings
from django.db.models.fields import Field


MSG = "[SKIPPED] Type of {} is not defined. HINT: Use alias method or set ALIASES to register type {}."


class MissingWarning(UserWarning):
    pass


def fallback(field, e):
    d2a_config = getattr(settings, 'D2A_CONFIG', {})
    missing = d2a_config.get('MISSING', MissingWarning)

    msg = MSG.format(field, type(field))
    if missing is MissingWarning:
        warnings.warn(msg, MissingWarning)
        return None

    return missing
