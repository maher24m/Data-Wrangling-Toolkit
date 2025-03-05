from django.apps import AppConfig


class ImportAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.import_app'

    def ready(self): 
        import api.import_app.registry