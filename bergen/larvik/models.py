import uuid

import zarr as zr
import dask
import xarray
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from larvik.logging import get_module_logger
from larvik.managers import ZarrManager
from larvik.storage.store import openDataset, getStore


logger = get_module_logger(__name__)


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


class Zarr(models.Model):
    store = models.FilePathField(max_length=600)
    group = models.CharField(max_length=800)

    objects = ZarrManager()

    @property
    def array(self):
        dataset = openDataset(self.store, self.group, chunks="auto")
        return dataset["data"]

    @property
    def info(self):
        dataset = openDataset(self.store, self.group)
        return dataset.info()

    def saveArray(self, array, compute=True, name="data")-> dask.delayed:
        return array.to_dataset(name=name).to_zarr(store=getStore(self.store), mode="w", group=self.group, compute=compute)

    def loadDataset(self, chunks="auto") -> xarray.Dataset:
        return openDataset(self.store, self.group, chunks=chunks)

    def openArray(self, name="data", chunks="auto") -> xarray.DataArray:
        dataset = openDataset(self.store, self.group)
        return dataset[name]

    def saveDataset(self, dataset, compute=True) -> dask.delayed:
        return dataset.to_zarr(store=getStore(self.store), mode="w", group=self.group,compute=compute)

    def delete(self, *args, **kwargs):

        super(Zarr, self).delete(*args, **kwargs)
        try:

            store = getStore(self.store)

            if zr.storage.contains_group(store, self.group):
                logger.info(f"Removing Group {self.group} from Store {self.store}")
                zr.storage.rmdir(store, self.group)
                logger.info(f"Removing Group {self.group} from Store {self.store}")
            else:
                logger.info(f"Group {self.group} in Store {self.store} does no longer Exist")
        except Exception as e:
            logger.error(f"Error while handling Store {self.store}: {e}")


    def __str__(self):
        return f"Zarr Group {self.group} at Store {self.store}"

    def _repr_html_(self):
        return "<h1>" + str(self.group) + "</h1>"




class LarvikArrayProxy(models.Model):
    zarr: Zarr = models.ForeignKey(Zarr, on_delete=models.CASCADE, blank=True, null=True)
    shape = models.CharField(max_length=100, blank=True, null= True)
    name = models.CharField(max_length=1000)
    signature = models.CharField(max_length=300,null=True, blank=True)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        abstract = True

    @property
    def array(self):
        if self.zarr:
            array =  self.zarr.openArray(chunks="auto", name="data")
            if self.name is not None:
                array.name = str(self.name)
            return array


