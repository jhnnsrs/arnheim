# import the logging library
import logging
import os
import random
import string

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from pandas import HDFStore

from mandal import settings

# Get an instance of a logger
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

class ZarrQueryMixin(object):
    """ Methods that appear both in the manager and queryset. """
    def delete(self):
        # Use individual queries to the attachment is removed.
        for zarr in self.all():
            zarr.delete()

class ZarrQuerySet(ZarrQueryMixin, QuerySet):
    pass

class ZarrManager(Manager):
    def get_queryset(self):
        return ZarrQuerySet(self.model, using=self._db)

    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def fromRequest(self, name="", store="", type="transformation", overwrite=True):
        #Test if instance Already Exists
        from django.template.defaultfilters import slugify

        group = type + "/" + slugify(name) if overwrite else type + "/" + slugify(name+self.id_generator())
        logger.info("Looking for Group {0}".format(group))
        try:
            item = super(ZarrManager,self).get(group=group,store=store)
            return item
        except ObjectDoesNotExist:
            return super(ZarrManager, self).create(store=store, group=group)



