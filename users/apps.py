from django.apps import AppConfig
class YourAppConfig(AppConfig):
    name = 'users'

    def ready(self):
        # Import signals here to ensure they are registered properly
        from . import signals