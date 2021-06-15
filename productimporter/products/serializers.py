import pathlib

import boto3
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import subprocess
from productimporter.products.models import Product
from productimporter.utils.helpers import make_base_url


class ProductSerializer(serializers.ModelSerializer):
    detail_page = serializers.SerializerMethodField()

    def get_detail_page(self,obj):
        return self.context + '/api/product/' + str(obj.id)

    class Meta:
        model = Product
        fields = ('detail_page','sku','name','description','active')


class DownloadProductsSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=255)

    def validate_key(self, key):
        if not key.endswith('.csv'):
            raise ValidationError("Invalid key extension.")
        return key

    def save(self, **kwargs):
        key = self.validated_data['key']
        filepath = self.download_file(key)
        # '''
        # reversing because we have to override the records if duplication in sku happens.
        # Rather than overriding, I will ignore the records that came before the last entry. that is handled in bulk_update of django.
        # Reversing so that the last record comes first and then the rest of the same records are ignored.
        # '''
        self.reverse_records(filepath)
        return filepath

    def download_file(self,key):

        s3_download_filepath = 'temp/' + key
        s3 = boto3.session.Session(
            region_name=settings.AWS_S3_REGION_NAME
        ).client('s3')
        pathlib.Path(s3_download_filepath.rsplit('/',1)[0]).mkdir(parents=True, exist_ok=True)
        s3.download_file(settings.AWS_STORAGE_BUCKET_NAME, key, s3_download_filepath)
        return s3_download_filepath

    def reverse_records(self,filepath):
        import pandas as pd

        # load the csv and user row 0 as headers
        df = pd.read_csv(filepath, header=0)

        # reverse the data
        df.iloc[::-1].to_csv(filepath,index=False)

