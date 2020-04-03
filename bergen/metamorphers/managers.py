import io
import json

import xarray
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models


def renormalize(n, range1, range2):
    delta1 = range1[1] - range1[0]
    delta2 = range2[1] - range2[0]
    return (delta2 * (n - range1[0]) / delta1) + range2[0]



class DisplayManager(models.Manager):

    def from_xarray_and_request(self, array: xarray.DataArray, request):
        # Do some extra stuff here on the submitted data before saving...
        # For example...
        img = Image.fromarray(array)
        img = img.convert('RGB')
        name = "Display of " + request.representation.name
        display = self.create(representation=request.representation,
                            name=name,
                            creator=request.creator,
                            nodeid=request.nodeid,
                            shape=json.dumps(list(array.shape)),)


        # TODO: update array of output
        path = f"representation-{display.representation.id}_node-{request.nodeid}"
        img_io = io.BytesIO()
        img.save(img_io, format='jpeg', quality=100)
        thumb_file = InMemoryUploadedFile(img_io, None, path + ".jpeg", 'image/jpeg',
                                          img_io.tell, None)

        display.image = thumb_file
        display.save()

        return display
