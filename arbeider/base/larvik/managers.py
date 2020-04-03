# import the logging library
import json
import logging
import xarray as xr
from django.db.models.manager import Manager
from django.db.models.query import QuerySet

# Get an instance of a logger
from larvik.generators import ArnheimGenerator

logger = logging.getLogger(__name__)

class ZarrQueryMixin(object):
    """ Methods that appear both in the manager and queryset. """


class ZarrQuerySet(QuerySet):

    def delete(self):
        # Use individual queries to the attachment is removed.
        for zarr in self.all():
            zarr.delete()


        super().delete()


class LarvikArrayManager(Manager):
    generatorClass = ArnheimGenerator
    group = None
    queryset = ZarrQuerySet

    def get_queryset(self):
        return self.queryset(self.model, using=self._db)


    def from_xarray(self, array: xr.DataArray, **kwargs):
        # Do some extra stuff here on the submitted data before saving...
        # For example...

        item = self.model(**kwargs)
        generated = self.generatorClass(item, self.group)
        array.name = generated.name

        # Store Generation
        item.store.name = generated.path
        item.shape = json.dumps(array.shape)

        # Actually Saving
        item.store.dump(array)
        item.save()
        return item

