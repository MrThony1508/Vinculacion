from django.apps import AppConfig

class LoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Aplicaciones.Login'

    def ready(self):
        import Aplicaciones.Login.signals

