import warnings

from django.conf import settings
from django.db.models.fields import Field


MSG = "[SKIPPED] Config of {} is not defined. HINT: Use alias method or set ALIASES."


class MissingWarning(UserWarning):
    pass


def fallback(field_type, e):
    d2a_config = getattr(settings, 'D2A_CONFIG', {})
    missing = d2a_config.get('MISSING', MissingWarning)

    msg = MSG.format(field_type.__name__)
    if missing is MissingWarning:
        warnings.warn(msg, MissingWarning)
        return None

    return missing
