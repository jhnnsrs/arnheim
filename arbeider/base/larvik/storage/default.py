from  django.conf import settings

from larvik.storage.local import LocalStorage
from larvik.storage.s3 import S3Storage


def get_default_storagemode():
    try:
        if (settings.STORAGE_MODE == "LOCAL"):
            return LocalStorage
        if (settings.STORAGE_MODE == "S3"):
            return S3Storage
        else:
            raise NotImplementedError("Storage Mode not Implemented: Try LOCAL or S3")
    except:
        raise NotImplementedError("Please specify a Storage Mode: STORAGE_MODE")