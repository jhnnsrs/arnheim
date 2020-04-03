import traceback

import xarray as xr
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models.fields.files import FieldFile
import zarr
from larvik.logging import get_module_logger
from storages.backends.s3boto3 import S3Boto3Storage
import s3fs

from zarr import blosc
logger = get_module_logger(__name__)


class LocalFile(object):
    def __init__(self, field, haspath=False):
        self.field = field
        self.tmppath = "/tmp"
        self.haspath = haspath

    def __enter__(self):
        if self.haspath: return self.field.path # No TempFile Necessary
        import os
        import uuid
        _, file_extension = os.path.splitext(self.field.name)
        self.filename = self.tmppath + "/" + str(uuid.uuid4()) + file_extension
        with open(self.filename, 'wb+') as destination:
            for chunk in self.field.chunks():
                destination.write(chunk)

        return self.filename

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            return False # uncomment to pass exception through
        if self.haspath:
            return True # We dont need a Temporary File of a Local File
        else:
            import os
            os.remove(self.filename)

        return True


class BioImageFile(FieldFile):

    @property
    def local(self):
        if isinstance(self.storage, S3Boto3Storage):
            return LocalFile(self, haspath=False)
        if isinstance(self.storage, FileSystemStorage):
            return LocalFile(self, haspath=True)
        else:
            raise NotImplementedError("Other Storage Formats have not been established yet. Please use S3 like Storage for time being")


compressor = blosc.Blosc(cname='zstd', clevel=3, shuffle=blosc.Blosc.BITSHUFFLE)
blosc.use_threads = True

zarr.storage.default_compressor = compressor

class XArrayStore(FieldFile):

    def _getStore(self):
        if isinstance(self.storage, S3Boto3Storage):
            bucket = self.storage.bucket_name
            location = self.storage.location
            s3_path = f"{bucket}/{self.name}"
            # Initilize the S3 file system
            logger.info(f"Bucket [{bucket}]: Connecting to {self.name}")
            s3 = s3fs.S3FileSystem(client_kwargs={"endpoint_url": settings.AWS_S3_ENDPOINT_URL})
            store = s3fs.S3Map(root=s3_path, s3=s3)
            return store
        if isinstance(self.storage, FileSystemStorage):
            location = self.storage.location
            path = f"{location}/{self.name}"
            # Initilize the S3 file system
            logger.info(f"Folder [{location}]: Connecting to {self.name}")
            store = zarr.DirectoryStore(path)
            return store
        else:
            raise NotImplementedError("Other Storage Formats have not been established yet. Please use S3 like Storage for time being")

    @property
    def connected(self):
        return self._getStore()

    def dump(self, array, compute=True,name="data"):
        return array.to_dataset(name=name).to_zarr(store=self.connected, mode="w", compute=compute)

    def load(self,name="data"):
        return xr.open_zarr(store=self.connected, consolidated=False)[name]