import os
from django.conf import settings
from celery import Celery
from celery.utils.nodenames import gethostname
# set the default Django settings module for the 'celery' program.


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("productimporter")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.task_acks_late = True
app.worker_prefetch_multiplier = 1

