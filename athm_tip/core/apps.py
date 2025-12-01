from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "athm_tip.core"

    def ready(self):
        from . import signals  # noqa: F401
