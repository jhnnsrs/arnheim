# import the logging library
import logging
import random
import string

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.manager import Manager
from django.db.models.query import QuerySet

# Get an instance of a logger
logger = logging.getLogger(__name__)

class ZarrQueryMixin(object):
    """ Methods that appear both in the manager and queryset. """


class ZarrQuerySet(QuerySet):

    def delete(self):
        # Use individual queries to the attachment is removed.
        for zarr in self.all():
            zarr.delete()


        super().delete()

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