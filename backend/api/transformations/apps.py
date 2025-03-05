from django.apps import AppConfig


class TransformationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.transformations'

    def ready(self):
        import api.transformations.registry
