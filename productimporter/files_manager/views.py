import base64
import hashlib
import hmac
import os
import time

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework import permissions, status, authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FileItem
from ..utils.csrf_exempt import CsrfExemptSessionAuthentication
from ..utils.storage import create_presigned_upload_url
from django.shortcuts import render, redirect

AWS_UPLOAD_BUCKET = settings.AWS_STORAGE_BUCKET_NAME
AWS_UPLOAD_REGION = settings.AWS_S3_REGION_NAME
AWS_UPLOAD_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_UPLOAD_SECRET_KEY = settings.AWS_SECRET_ACCESS_KEY
from django.views.generic import TemplateView

@csrf_exempt
def my_view(request):
    return TemplateView('Hello world')



class FilePolicyAPI(APIView):
    """
    This view is to get the AWS Upload Policy for our s3 bucket.
    What we do here is first create a FileItem object instance in our
    Django backend. This is to include the FileItem instance in the path
    we will use within our bucket as you'll see below.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, *args, **kwargs):

        filename_req = request.data.get('filename')
        if not filename_req:
            print({"message": "A filename is required"})
            return Response({"message": "A filename is required"}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        username_str = str(request.user.username)
        """
        Below we create the Django object. We'll use this
        in our upload path to AWS.

        Example:
        To-be-uploaded file's name: Some Random File.mp4
        Eventual Path on S3: <bucket>/username/2312/2312.mp4
        """
        file_obj = FileItem.objects.create(user=user, name=filename_req)
        file_obj_id = file_obj.id
        upload_start_path = "{username}/{file_obj_id}/".format(
            username=username_str,
            file_obj_id=file_obj_id
        )
        _, file_extension = os.path.splitext(filename_req)
        filename_final = "{file_obj_id}{file_extension}".format(
            file_obj_id=file_obj_id,
            file_extension=file_extension

        )
        """
        Eventual file_upload_path includes the renamed file to the
        Django-stored FileItem instance ID. Renaming the file is
        done to prevent issues with user generated formatted names.
        """
        final_upload_path = "{upload_start_path}{filename_final}".format(
            upload_start_path=upload_start_path,
            filename_final=filename_final,
        )
        if filename_req and file_extension:
            """
            Save the eventual path to the Django-stored FileItem instance
            """
            file_obj.path = final_upload_path
            file_obj.save()

        data = create_presigned_upload_url(AWS_UPLOAD_BUCKET, file_obj.path)
        data['file_item_id'] = file_obj_id

        print("DATA: ", data)

        return Response(data, status=status.HTTP_200_OK)
