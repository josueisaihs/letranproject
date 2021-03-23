from django.apps import AppConfig


class DocenciaConfig(AppConfig):
    name = 'Docencia'

    def ready(self):
        from . import signals
