import time
import threading

from django.apps import AppConfig


class D2aConfig(AppConfig):
    name = 'd2a'

    def ready(self):
        import d2a
        t = threading.Thread(target=d2a.autoload)
        t.start()
        t.join()
