from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    bucket_name = 'media'
    custom_domain = f"localhost:9153/{bucket_name}"


class ZarrStorage(S3Boto3Storage):
    bucket_name = 'zarr'
    custom_domain = f"localhost:9153/{bucket_name}"



class FilesStorage(S3Boto3Storage):
    bucket_name = 'files'
    custom_domain = f"localhost:9153/{bucket_name}"
