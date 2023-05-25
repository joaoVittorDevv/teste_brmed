import os
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("teste_brmed")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    'buscar_url': {
        'task': 'core.tasks.fetch_new_data',
        # 'schedule': crontab(hour=18, minute=30),
        'schedule':timedelta(minutes=1)
    },
}

app.autodiscover_tasks()
