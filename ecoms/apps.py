from django.apps import AppConfig


class EcomsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ecoms"
    def ready(self):
        import ecoms.signals