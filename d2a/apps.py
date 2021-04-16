import time
import threading

from django.apps import AppConfig


class D2aConfig(AppConfig):
    name = 'd2a'

    def ready(self):
        import d2a
        if d2a.D2A_CONFIG.get("AUTOLOAD") in (False, None):
            return

        t = threading.Thread(target=d2a.autoload)
        t.start()
        t.join()
