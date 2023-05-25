from django.apps import AppConfig
from .data_fetcher import fetch_data
from django.db.models.signals import post_migrate


def execute_after_migrations(sender, **kwargs):
    fetch_data()


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        post_migrate.connect(execute_after_migrations, sender=self)
