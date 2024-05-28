from django.apps import AppConfig


class ProtoauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'protoAuth'

    def ready(self):
        import protoAuth.signals