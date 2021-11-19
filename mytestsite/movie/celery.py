import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mytestsite.settings")

app = Celery("mytestsite", backend="redis", broker="redis://3.70.18.96:6379")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()