import logging
import pandas as pd

from productimporter.products.models import Product
from productimporter.utils.helpers import generate_lazy_objs

logger = logging.getLogger(__name__)

import celery
from celery.task import task

class BaseClassForTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # exc (Exception) - The exception raised by the task.
        # args (Tuple) - Original arguments for the task that failed.
        # kwargs (Dict) - Original keyword arguments for the task that failed.
        print('{0!r} failed: {1!r}'.format(task_id, exc))


@task(name="bulk_create_iter",soft_time_limit=10000,time_limit=20000)
def bulk_create_iter(df):
    df = pd.read_json(df)
    objs = generate_lazy_objs(df)
    Product.objects.bulk_create(objs, ignore_conflicts=True)


