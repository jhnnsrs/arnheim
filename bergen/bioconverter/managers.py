import os

from django.contrib.auth.models import User
from django.db import models

from elements.models import Sample, Numpy, Zarr
from mandal import settings
import xarray

class RepresentationManager(models.Manager):

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
        store = os.path.join(settings.ZARR_ROOT, "sample-{0}".format(sample.id))
        zarr = Zarr.objects.fromRequest(name=name, store=store, type="representation", overwrite=overwrite)
        delayed = zarr.saveArray(array,compute=compute)

            # Now call the super method which does the actual creation
        if compute:
            return super().create(name=name,#
                                  creator=creator,
                                  sample= sample,
                                  inputrep=inputrep,
                                  numpy= None,
                                  zarr= zarr,
                                  experiment=experiment,
                                  nodeid=nodeid)  # Python 3 syntax!!
        else:
            return super().create(name=name,  #
                                  creator=creator,
                                  sample=sample,
                                  inputrep=inputrep,
                                  numpy=None,
                                  zarr=zarr,
                                  experiment=experiment,
                                  nodeid=nodeid), delayed
