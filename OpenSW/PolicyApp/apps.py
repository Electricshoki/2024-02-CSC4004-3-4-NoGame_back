from django.apps import AppConfig


class PolicyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PolicyApp'
    
    def ready(self):
        import PolicyApp.signals
