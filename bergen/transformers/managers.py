from django.db import models

from elements.models import Sample, Numpy


class TransformationManager(models.Manager):
    def create(self, **obj_data):
        # Do some extra stuff here on the submitted data before saving...
        # For example...
        if "nparray" in obj_data:
            print("Creating Representation with help of np.array")
            sample: Sample = obj_data["sample"]
            vid = str(obj_data["vid"])

            # TODO: if sample is not provided this should raise an exception
            numpy = Numpy.objects.create(vid=vid, numpy=obj_data["nparray"], sample=sample, type="transformations", dtype=obj_data["dtype"], compression=obj_data["compression"])

            obj_data["numpy"] = numpy
            del obj_data["nparray"]

        # Now call the super method which does the actual creation
        return super().create(**obj_data)  # Python 3 syntax!!