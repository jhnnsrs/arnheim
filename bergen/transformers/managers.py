import os

import xarray
from django.contrib.auth.models import User
from django.db import models
from django.db.models.manager import BaseManager, Manager
from django.db.models.query import QuerySet

from elements.models import Sample, Zarr
from mandal import settings


class TransformationManager(models.Manager):

    def from_xarray(self, array: xarray.DataArray,
                    sample: Sample= None,
                    name: str ="Initial Stack",
                    overwrite=True,
                    creator: User = None,
                    inputrep = None,
                    experiment = None,
                    nodeid= None,
                    compute=True):
        # Do some extra stuff here on the submitted data before saving...
        # For example...
        store = os.path.join(settings.ZARR_ROOT, "sample-{0}".format(sample.id))
        zarr = Zarr.objects.fromRequest(name=name, store=store, type="transformation", overwrite=overwrite)
        delayed = zarr.saveArray(array,compute=compute)

            # Now call the super method which does the actual creation
        if compute:
            return super().create(name=name,#
                                  creator=creator,
                                  sample= sample,
                                  inputrep=inputrep,
                                  numpy= None,
                                  zarr= zarr,
                                  experiment=experiment,
                                  nodeid=nodeid)  # Python 3 syntax!!
        else:
            return super().create(name=name,  #
                                  creator=creator,
                                  sample=sample,
                                  inputrep=inputrep,
                                  numpy=None,
                                  zarr=zarr,
                                  experiment=experiment,
                                  nodeid=nodeid), delayed



class DistributedTransformationQuerySet(QuerySet):

    def asArrays(self,*args, **kwargs):
        import dask.bag as db

        obj = self._clone()
        if obj._sticky_filter:
            obj.query.filter_is_sticky = True
            obj._sticky_filter = False
        obj.__dict__.update(kwargs)
        return db.from_sequence([item.zarr.openArray() for item in obj])



class DistributedTransformationManager(Manager):

    def get_queryset(self):
        return DistributedTransformationQuerySet(self.model, using=self._db)

    def from_xarray(self, array: xarray.DataArray,
                    sample: Sample= None,
                    name: str ="Initial Stack",
                    overwrite=True,
                    creator: User = None,
                    inputrep = None,
                    experiment = None,
                    nodeid= None,
                    compute=True):
        # Do some extra stuff here on the submitted data before saving...
        # For example...
        store = os.path.join(settings.ZARR_ROOT, "sample-{0}".format(sample.id))
        zarr = Zarr.objects.fromRequest(name=name, store=store, type="transformation", overwrite=overwrite)
        delayed = zarr.saveArray(array,compute=compute)

            # Now call the super method which does the actual creation
        if compute:
            return super().create(name=name,#
                                  creator=creator,
                                  sample= sample,
                                  inputrep=inputrep,
                                  numpy= None,
                                  zarr= zarr,
                                  experiment=experiment,
                                  nodeid=nodeid)  # Python 3 syntax!!
        else:
            return super().create(name=name,  #
                                  creator=creator,
                                  sample=sample,
                                  inputrep=inputrep,
                                  numpy=None,
                                  zarr=zarr,
                                  experiment=experiment,
                                  nodeid=nodeid), delayed