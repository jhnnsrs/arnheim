import uuid

import zarr as zr
import dask
import xarray
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

# Create your models here.
from larvik.fields import StoreFileField
from larvik.logging import get_module_logger
from larvik.managers import LarvikArrayManager
from larvik.storage.default import get_default_storagemode
from larvik.storage.local import ZarrStorage, LocalStorage
from larvik.storage.s3 import S3Storage

logger = get_module_logger(__name__)

get_user_model()
class LarvikJob(models.Model):
    statuscode = models.IntegerField( null=True, blank=True)
    statusmessage = models.CharField(max_length=500,  null=True, blank=True)
    settings = models.CharField(max_length=1000) # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    nodeid = models.CharField(max_length=400, null=True, blank=True)

    class Meta:
        abstract = True

    def _repr_html_(self):
        return f'''<h5>Request by {self.creator.username} </h5>
                <ul>
                    <li> Last Status: {self.statusmessage}</li>
                    <li> Node Status: {self.nodeid}</li>
                    <li> Settings: {self.settings}</li>
                </ul>'''

class LarvikConsumer(models.Model):
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, unique=True, default="Not active")
    settings = models.CharField(max_length=1000)  # json decoded standardsettings

    class Meta:
        abstract = True


class LarvikArrayProxy(models.Model):

    store = StoreFileField(verbose_name="store",storage=get_default_storagemode().zarr(), upload_to="zarr", blank=True, null= True, help_text="The location of the Array on the Storage")
    shape = models.CharField(max_length=100, blank=True, null= True)
    name = models.CharField(max_length=1000, blank=True, null= True)
    signature = models.CharField(max_length=300,null=True, blank=True)


    objects = LarvikArrayManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        abstract = True

    @property
    def info(self):
        return self.array.info()

    @property
    def viewer(self):
        import larvik.extenders
        return self.array.viewer

    @property
    def biometa(self):
        import larvik.extenders
        return self.array.biometa

    @property
    def array(self):
        if self.store:
            array = self.store.load(chunks="auto", name="data")
            return array
        else:
            raise NotImplementedError("This array does not have a store")

    def _repr_html_(self):
        return "<h1>" + f'Array at {str(self.group)} in {self.store}' + "</h1>"


