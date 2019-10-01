# import the logging library
import logging
import os

import h5py
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