import io
import json

import xarray
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models



class ReflectionManager(models.Manager):

    def from_xarray_and_request(self, array: xarray.DataArray, request):
        # Do some extra stuff here on the submitted data before saving...
        # For example...
        img = Image.fromarray(array)
        img = img.convert('RGB')
        name = "Request of " + request.transformation.name
        reflection = self.create(transformation=request.transformation,
                            name=name,
                            creator=request.creator,
                            nodeid=request.nodeid,
                            shape=json.dumps(list(array.shape)),)


        # TODO: update array of output
        path = f"transformation-{reflection.transformation.id}_node-{request.nodeid}"
        img_io = io.BytesIO()
        img.save(img_io, format='jpeg', quality=100)
        thumb_file = InMemoryUploadedFile(img_io, None, path + ".jpeg", 'image/jpeg',
                                          img_io.tell, None)

        reflection.image = thumb_file
        reflection.save()

        return reflection
