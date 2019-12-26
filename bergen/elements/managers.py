# import the logging library
import logging
import os
import string
import random
import zarr
import h5py
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from pandas import HDFStore

from elements.utils import toFileName
from mandal import settings

# Get an instance of a logger
logger = logging.getLogger(__name__)


class NumpyManager(models.Manager):

    def create(self, **obj_data):
        if obj_data["numpy"] is not None:
            joinedpath = os.path.join(settings.H5FILES_ROOT, toFileName(obj_data["sample"]))
            if not os.path.exists(settings.H5FILES_ROOT):
                logger.warning("Creating Directory for H5Files"+str(settings.H5FILES_ROOT))
                os.makedirs(settings.H5FILES_ROOT)

            type = obj_data["type"]
            vid = obj_data["vid"]
            dtype = obj_data["dtype"] if obj_data["dtype"] else None
            compression = obj_data["compression"] if obj_data["compression"] else None
            with h5py.File(joinedpath, 'a') as hf:
                if not type in hf: hf.create_group(type)
                hf_group = hf[type]
                if vid in hf_group: del hf_group[vid]
                hf_group.create_dataset(vid, data=obj_data["numpy"], dtype=dtype, compression=compression)
                obj_data["filepath"] = joinedpath

            del obj_data["numpy"]


        return super(NumpyManager,self).create(**obj_data)

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


class ZarrManager(models.Manager):

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



