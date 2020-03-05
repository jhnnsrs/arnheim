# import the logging library
import logging
import os

import xarray
from django.contrib.auth.models import User
from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from elements.utils import buildRepresentationName, buildTransformationName
from larvik.models import Zarr
from larvik.querysets import LarvikArrayQueryset
from django.db import models

# TODO: Realiance on HDF5 Store should be nulled
from pandas import HDFStore

from django.conf import settings

# Get an instance of a logger}
logger = logging.getLogger(__name__)




class PandasManager(models.Manager):

    def create(self, **obj_data):
        if obj_data["dataframe"] is not None:
            joinedpath = os.path.join(settings.PANDAS_ROOT, obj_data["answer"] + ".h5")
            if not os.path.exists(settings.PANDAS_ROOT):
                logger.warning("Creating Directory for Pandas"+str(settings.PANDAS_ROOT))
                os.makedirs(settings.PANDAS_ROOT)

            type = obj_data["type"] if obj_data["type"] else "answers"
            vid = obj_data["vid"]
            compression = obj_data["compression"] if obj_data["compression"] else None
            with HDFStore(joinedpath) as store:
                path = type + "/" + vid
                store.put(path,obj_data["dataframe"])
                obj_data["filepath"] = joinedpath
                #TODO: Implement Compression here


            del obj_data["dataframe"]

        return super(PandasManager,self).create(**obj_data)


class RepQueryMixin(object):
    """ Methods that appear both in the manager and queryset. """
    def delete(self):
        # Use individual queries to the attachment is removed.
        for rep in self.all():
            rep.delete()

class RepresentationQuerySet(LarvikArrayQueryset):

    def _repr_html_(self):
        from django.template.loader import render_to_string
        count = self.count()
        limit = 3
        if count < limit:
            return render_to_string('ipython/representation.html', {'representations': self, "more": 0})
        else:
            return render_to_string('ipython/representation.html', {'representations': self[:limit], "more": count - limit})


class RepresentationManager(Manager):

    def get_queryset(self):
        return LarvikArrayQueryset(self.model, using=self._db)

    def from_xarray(self, array: xarray.DataArray,
                    name: str ="Initial Stack",
                    sample = None,
                    creator: User = None,
                    inputrep = None,
                    nodeid= None,
                    **kwargs):
        # Do some extra stuff here on the submitted data before saving...
        # For example...

        zarrname = buildRepresentationName(name, nodeid)
        store = os.path.join(settings.ZARR_ROOT, "sample-{0}".format(sample.id))
        zarr = Zarr.objects.fromRequest(name=zarrname, store=store, type="representation", overwrite=True)
        delayed = zarr.saveArray(array,compute=True)

            # Now call the super method which does the actual creation
        return super().create(name=name,
                              zarr= zarr,
                              creator=creator,
                              sample= sample,
                              inputrep=inputrep,
                              nodeid=nodeid,
                              **kwargs)
        # Python 3 syntax!!



class DelayedRepresentationManager(Manager):


    def get_queryset(self):
        return RepresentationQuerySet(self.model, using=self._db)


    def from_xarray(self, array: xarray.DataArray,
                    sample = None,
                    name: str ="Initial Stack",
                    overwrite=True,
                    creator: User = None,
                    inputrep = None,
                    nodeid= None,
                    **kwargs):
        # Do some extra stuff here on the submitted data before saving...
        # For example...
        zarrname = buildRepresentationName(name, nodeid)
        store = os.path.join(settings.ZARR_ROOT, "sample-{0}".format(sample.id))
        zarr = Zarr.objects.fromRequest(name=zarrname, store=store, type="representation", overwrite=overwrite)
        delayed = zarr.saveArray(array,compute=False)

        # Now call the super method which does the actual creation
        return super().create(name=name,  #
                              creator=creator,
                              sample=sample,
                              inputrep=inputrep,
                              zarr=zarr,
                              nodeid=nodeid,), delayed


    def from_xarray_and_request(self, array: xarray.DataArray, request, name: str= None, **kwargs):
        return self.from_xarray(array,
                                sample=request.sample,
                                name=name,
                                creator=request.creator,
                                inputrep=request.representation,
                                nodeid=request.nodeid)



class TransformationManager(models.Manager):

    def from_xarray(self, array: xarray.DataArray,
                    name: str ="transformation",
                    overwrite=True,
                    creator: User = None,
                    representation = None,
                    nodeid= None):
        # Do some extra stuff here on the submitted data before saving...
        # For example...
        zarrname = buildTransformationName(name, nodeid)
        store = os.path.join(settings.ZARR_ROOT, "sample-{0}".format(representation.sample.id))
        zarr = Zarr.objects.fromRequest(name=zarrname, store=store, type="transformation", overwrite=overwrite)
        delayed = zarr.saveArray(array,compute=True)

        return super().create(name=name,#
                              creator=creator,
                              representation=representation,
                              zarr= zarr,
                              nodeid=nodeid)  # Python 3 syntax!!




class DistributedTransformationQuerySet(QuerySet):

    def asArrays(self,*args, **kwargs):
        import dask.bag as db

        obj = self._clone()
        if obj._sticky_filter:
            obj.query.filter_is_sticky = True
            obj._sticky_filter = False
        obj.__dict__.update(kwargs)
        return db.from_sequence([item.zarr.openArray() for item in obj])



class DelayedTransformationManager(Manager):

    def get_queryset(self):
        return DistributedTransformationQuerySet(self.model, using=self._db)

    def from_xarray(self, array: xarray.DataArray,
                    name: str ="transformation",
                    overwrite=True,
                    creator: User = None,
                    representation = None,
                    transformer = None,
                    inputtransformation = None,
                    roi = None,
                    nodeid= None):
        # Do some extra stuff here on the submitted data before saving...
        # For example...
        zarrname = buildTransformationName(roi, representation, transformer, inputtransformation, nodeid)
        store = os.path.join(settings.ZARR_ROOT, "sample-{0}".format(representation.sample.id))
        zarr = Zarr.objects.fromRequest(name=zarrname, store=store, type="transformation", overwrite=overwrite)
        delayed = zarr.saveArray(array,compute=False)

            # Now call the super method which does the actual creation
        return super().create(name=name,  #
                                  creator=creator,
                                  representation=representation,
                                  roi=roi,
                                  inputtransformation=inputtransformation,
                                  zarr=zarr,
                                  nodeid=nodeid), delayed





