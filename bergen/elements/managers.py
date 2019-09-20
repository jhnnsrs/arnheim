# import the logging library
import logging
import os

import h5py
from django.db import models

from multichat import settings

# Get an instance of a logger
logger = logging.getLogger(__name__)

def toFileName(sampleName):
    return sampleName + ".h5"

class NumpyManager(models.Manager):

    def create(self, **obj_data):
        if obj_data["numpy"] is not None:
            directory = os.path.join(settings.MEDIA_ROOT + "/h5files/")
            joinedpath = os.path.join(directory, toFileName(obj_data["sample"].name))
            if not os.path.exists(directory):
                logger.warning("Creating Directory "+str(directory))
                os.makedirs(directory)

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