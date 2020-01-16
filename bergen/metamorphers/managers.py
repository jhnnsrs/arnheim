import io

import xarray
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from filterbank.logic.addins import toimage


class DisplayManager(models.Manager):

    def from_xarray_and_request(self, array: xarray.DataArray, request):
        # Do some extra stuff here on the submitted data before saving...
        # For example...

        name = "Display of " + request.representation.name
        image = toimage(array)

        display = self.create(representation=request.representation,
                            name=name,
                            creator=request.creator,
                            nodeid=request.nodeid,
                            sample=request.sample,
                            shape=request.representation.shape,
                            experiment=request.representation.experiment)


        # TODO: update array of output
        path = "sample-{0}_representation-{1}_node-{2}".format(str(display.sample.id), str(display.representation.id),
                                                               str(request.nodeid))
        img_io = io.BytesIO()
        image.save(img_io, format='jpeg', quality=100)
        thumb_file = InMemoryUploadedFile(img_io, None, path + ".jpeg", 'image/jpeg',
                                          img_io.tell, None)

        display.image = thumb_file
        display.save()

        return display
