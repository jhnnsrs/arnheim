import os

import xarray
import dask.bag as db
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from elements.models import Sample, Zarr
from elements.storage.store import openDataset
from larvik.querysets import LarvikArrayQueryset


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
                    sample: Sample= None,
                    name: str ="Initial Stack",
                    overwrite=True,
                    creator: User = None,
                    inputrep = None,
                    experiment = None,
                    nodeid= None,
                    compute=True,
                    **kwargs):
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
                                  zarr= zarr,
                                  experiment=experiment,
                                  nodeid=nodeid,
                                  **kwargs)
        # Python 3 syntax!!



class DistributedRepresentationManager(Manager):


    def get_queryset(self):
        return RepresentationQuerySet(self.model, using=self._db)


    def from_xarray(self, array: xarray.DataArray,
                    sample: Sample= None,
                    name: str ="Initial Stack",
                    overwrite=True,
                    creator: User = None,
                    inputrep = None,
                    experiment = None,
                    nodeid= None,
                    **kwargs):
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
                                  zarr=zarr,
                                  experiment=experiment,
                                  nodeid=nodeid,
                                  **kwargs), delayed


    def from_xarray_and_request(self, array: xarray.DataArray, request, name: str= None, **kwargs):
        return self.from_xarray(array,
                                sample=request.sample,
                                name=name,
                                creator=request.creator,
                                inputrep=request.representation,
                                nodeid=request.nodeid,
                                **kwargs)

