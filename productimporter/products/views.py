
from productimporter.utils.helpers import generate_lazy_objs, make_base_url
from celery import current_app
import json
import time
from datetime import datetime
from django.conf import settings
from django.http import StreamingHttpResponse
import pandas as pd
import awswrangler as wr
import boto3
from django.http.response import HttpResponse
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from productimporter.files_manager.models import FileItem
from productimporter.products.api import ProductViewSet
from productimporter.products.models import Product
from productimporter.utils.async_tasks import bulk_create_iter
from productimporter.utils.helpers import generate_lazy_objs


def process_csv_stream(request):
    file_id = request.GET.get('file_id','')

    if file_id:
        key = "temp/" + FileItem.objects.get(id=file_id).path
    else:
        raise ValidationError("Please provide a file_id")

    chunksize = settings.CHUNKSIZE
    lines_processed = [0] # mutable datatype so that nested function can mutate it

    def process(lines_processed):
        start_time = datetime.now()
        try:
            dfs = pd.read_csv(key,chunksize=chunksize)
        except Exception as e:
            yield 'Error: "Invalid file type"'
            raise ValidationError("Invalid file type")
        yield 'Loading data from csv, please wait'

        for df in dfs:
            lines_processed[0] += df.__len__()
            df = df.to_json()
            bulk_create_iter.apply_async(args=(df,),ignore_result=False,)
            yield "."
        # while current_app.tasks.keys():
        #     yield "."
        #     time.sleep(1)
        products_crud_url = make_base_url(request) + '/api/product'
        time_taken = (datetime.now() - start_time).seconds
        yield '\n%s rows queued to be saved. \nseconds taken: %s \ncurrent_time:%s\nGo to %s for other operations\n' % (str(lines_processed[0]), time_taken, datetime.now(), products_crud_url)
    return StreamingHttpResponse(process(lines_processed), content_type='text/event-stream')



