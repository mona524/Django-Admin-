from django.apps import AppConfig

class App02Config(AppConfig):
    name = 'custom'

    def ready(self):
        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('custom')
