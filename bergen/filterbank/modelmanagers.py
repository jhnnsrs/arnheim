import os

import h5py
from django.db import models

from multichat import settings


class NpArrayManager(models.Manager):

    def create(self, **obj_data):
        if obj_data["nparray"] is not None:
            joinedpath = os.path.join(settings.MEDIA_ROOT + "/representation_h5files/", obj_data["filepath"])
            with h5py.File(joinedpath, 'a') as hf:
                if not "representations" in hf: hf.create_group("representations")
                hfr = hf["representations"]
                if obj_data["position"] in hfr: del hfr[obj_data["position"]]
                hfr.create_dataset(obj_data["position"], data=obj_data["nparray"])
                obj_data["file"] = joinedpath

            del obj_data["nparray"]
            del obj_data["filepath"]

        return super(NpArrayManager,self).create(**obj_data)


