import importlib
from django.core.management import call_command


def test_sqla_codegen():
    call_command("sqla_codegen")
    import models_sqla
    importlib.reload(models_sqla)
