from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = settings.MEDIA_BUCKET
    custom_domain = f"localhost:9153/{bucket_name}"


class ZarrStorage(S3Boto3Storage):
    bucket_name = settings.ZARR_BUCKET
    custom_domain = f"localhost:9153/{bucket_name}"


class FilesStorage(S3Boto3Storage):
    bucket_name = settings.FILES_BUCKET
    custom_domain = f"localhost:9153/{bucket_name}"


class S3Storage():
    media = MediaStorage
    zarr = ZarrStorage
    files = FilesStorage