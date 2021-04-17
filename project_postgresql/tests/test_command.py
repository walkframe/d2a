import importlib
from django.core.management import call_command


def test_sqla_codegen():
    call_command("sqla_codegen")
    import models_sqla
    importlib.reload(models_sqla)


def test_save_original_template():
    from d2a.template import TEMPLATE
    with open("./original_template.tmpl", "w") as f:
        f.write(TEMPLATE)
