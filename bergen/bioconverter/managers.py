import os

import xarray
from django.contrib.auth.models import User
from django.db import models
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet

from elements.models import Numpy, Sample, Zarr
from django.conf import settings


def buildZarrName(name, nodeid):
    if nodeid is not None:
        return f"{name} {nodeid}"
    else:
        return f"{name}"

class RepQueryMixin(object):
    """ Methods that appear both in the manager and queryset. """
    def delete(self):
        # Use individual queries to the attachment is removed.
        for rep in self.all():
            rep.delete()

class RepresentationQuerySet(RepQueryMixin, QuerySet):
    pass

class RepresentationManager(BaseManager.from_queryset(RepresentationQuerySet)):

    def create(self, **obj_data):
        # Do some extra stuff here on the submitted data before saving...
        # For example...
        if "nparray" in obj_data:
            print("Creating Representation with help of np.array")
            sample: Sample = obj_data["sample"]
            vid = str(obj_data["vid"])

            # TODO: if sample is not provided this should raise an exception
            numpy = Numpy.objects.create(vid=vid,
                                         numpy=obj_data["nparray"],
                                         sample=sample,
                                         iszarr=False,
                                         type="representation",
                                         dtype=obj_data.get("dtype",settings.REPRESENTATION_DTYPE),
                                         compression=obj_data.get("compression", settings.REPRESENTATION_COMPRESSION)
                                         )

            obj_data["numpy"] = numpy
            del obj_data["nparray"]


        # Now call the super method which does the actual creation
        return super().create(**obj_data)  # Python 3 syntax!!

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

        zarrname = buildZarrName(name, nodeid)
        store = os.path.join(settings.ZARR_ROOT, "sample-{0}".format(sample.id))
        zarr = Zarr.objects.fromRequest(name=name, store=store, type="representation", overwrite=overwrite)
        delayed = zarr.saveArray(array,compute=True)

            # Now call the super method which does the actual creation
        return super().create(name=name,#
                                  creator=creator,
                                  sample= sample,
                                  inputrep=inputrep,
                                  numpy= None,
                                  zarr= zarr,
                                  experiment=experiment,
                                  nodeid=nodeid)  # Python 3 syntax!!







class DistributedRepresentationQuerySet(QuerySet):

    def asArrays(self,*args, **kwargs):
        import dask.bag as db

        obj = self._clone()
        if obj._sticky_filter:
            obj.query.filter_is_sticky = True
            obj._sticky_filter = False
        obj.__dict__.update(kwargs)
        return db.from_sequence([item.zarr.openArray() for item in obj])



class DistributedRepresentationManager(BaseManager.from_queryset(DistributedRepresentationQuerySet)):

    def create(self, **obj_data):
        # Do some extra stuff here on the submitted data before saving...
        # For example...
        if "nparray" in obj_data:
            print("Creating Representation with help of np.array")
            sample: Sample = obj_data["sample"]
            vid = str(obj_data["vid"])

            # TODO: if sample is not provided this should raise an exception
            numpy = Numpy.objects.create(vid=vid,
                                         numpy=obj_data["nparray"],
                                         sample=sample,
                                         iszarr=False,
                                         type="representation",
                                         dtype=obj_data.get("dtype",settings.REPRESENTATION_DTYPE),
                                         compression=obj_data.get("compression", settings.REPRESENTATION_COMPRESSION)
                                         )

            obj_data["numpy"] = numpy
            del obj_data["nparray"]


        # Now call the super method which does the actual creation
        return super().create(**obj_data)  # Python 3 syntax!!

    def from_xarray(self, array: xarray.DataArray,
                    sample: Sample= None,
                    name: str ="Initial Stack",
                    overwrite=True,
                    creator: User = None,
                    inputrep = None,
                    experiment = None,
                    nodeid= None):
        # Do some extra stuff here on the submitted data before saving...
        # For example...
        zarrname = buildZarrName(name, nodeid)
        store = os.path.join(settings.ZARR_ROOT, "sample-{0}".format(sample.id))
        zarr = Zarr.objects.fromRequest(name=zarrname, store=store, type="representation", overwrite=overwrite)
        delayed = zarr.saveArray(array,compute=False)

        # Now call the super method which does the actual creation
        return super().create(name=name,  #
                                  creator=creator,
                                  sample=sample,
                                  inputrep=inputrep,
                                  numpy=None,
                                  zarr=zarr,
                                  experiment=experiment,
                                  nodeid=nodeid), delayed


    def from_xarray_and_request(self, array: xarray.DataArray, request, name: str= None):
        return self.from_xarray(array,
                                sample=request.sample,
                                name=name,
                                creator=request.creator,
                                inputrep=request.representation,
                                nodeid=request.nodeid)

