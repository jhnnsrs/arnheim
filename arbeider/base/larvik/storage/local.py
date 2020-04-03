from django.core.files.storage import FileSystemStorage



class MediaStorage(FileSystemStorage):
    pass

class ZarrStorage(FileSystemStorage):
    pass

class FilesStorage(FileSystemStorage):
    pass


class LocalStorage():
    media = MediaStorage
    zarr = ZarrStorage
    files = FilesStorage