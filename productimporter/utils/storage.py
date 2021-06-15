import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from boto3.s3.transfer import TransferConfig
from storages.backends.s3boto3 import S3Boto3Storage
import logging

class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    file_overwrite = False


def create_presigned_upload_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """


    # Generate a presigned URL for the S3 object
    s3 = boto3.session.Session(
                             # config= boto3.session.Config(s3={'addressing_style': 'path'}),
                             # aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             # aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                             region_name=settings.AWS_S3_REGION_NAME
                             ).client('s3',
                                      endpoint_url='https://s3.' + settings.AWS_S3_REGION_NAME + '.amazonaws.com',
                                      config= boto3.session.Config(signature_version='s3v4'),)
    try:
        response = s3.generate_presigned_post(Bucket=bucket_name,
                                                     Key=object_name,
                                                     Fields={
                                                         'acl': 'private',
                                                         'Content-Type': 'binary/octet-stream',
                                                         # 'Content-MD5': str(md5),
                                                     },
                                                     Conditions=[
                                                         {"acl": "private"},
                                                         ["starts-with", "$Content-Type", ""],
                                                         # ["starts-with", "$Content-MD5", ""]
                                                     ]
                                                    )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


