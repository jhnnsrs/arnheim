import os

import h5py
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from drawing.models import Sample, ROI
from filterbank.models import NpArray, AImage, Representation
from multichat import settings
from representations.models import Experiment


class NumpyManager(models.Manager):

    def create(self, **obj_data):
        if obj_data["numpy"] is not None:
            joinedpath = os.path.join(settings.MEDIA_ROOT + "/h5files/", obj_data["sample"].name + ".h5")
            with h5py.File(joinedpath, 'a') as hf:
                if not obj_data["type"] in hf: hf.create_group(obj_data["type"])
                hfr = hf[obj_data["type"]]
                if obj_data["position"] in hfr: del hfr[obj_data["position"]]
                hfr.create_dataset(obj_data["position"], data=obj_data["numpy"])
                obj_data["file"] = joinedpath

            del obj_data["numpy"]

        return super(NumpyManager,self).create(**obj_data)


class Numpy(models.Model):
    file = models.FilePathField() # aka h5files/$sampleid.h5
    position = models.CharField(max_length=100) # aca vid0, vid1, vid2, vid3
    type = models.CharField(max_length=100)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    # Custom Manager to simply create an array
    objects = NumpyManager()

    def get_array(self):
        with h5py.File(self.file, 'a') as file:
            print("Trying to access file {0} to get array".format(self.file))
            hf = file[self.type]
            array = hf.get(self.position).value
        return array

    def set_array(self,array):
        with h5py.File(self.file, 'a') as file:
            print("Trying to access file {0} to set array".format(self.file))
            hf = file[self.type]
            if self.position in hf: del hf[self.position]
            hf.create_dataset(self.position, data=array)



class TransformationManager(models.Manager):
    def create(self, **obj_data):
        # Do some extra stuff here on the submitted data before saving...
        # For example...
        if "nparray" in obj_data:
            print("Creating Representation with help of np.array")
            sample: Sample = obj_data["sample"]
            position = str(obj_data["vid"])

            # TODO: if sample is not provided this should raise an exception
            numpy = Numpy.objects.create(position=position, numpy=obj_data["nparray"],sample=sample,type="transformations")

            obj_data["numpy"] = numpy
            del obj_data["nparray"]

        # Now call the super method which does the actual creation
        return super().create(**obj_data)  # Python 3 syntax!!


class Transformation(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    vid = models.CharField(max_length=200)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    shape = models.CharField(max_length=100, blank=True, null= True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='transformations')
    numpy = models.ForeignKey(Numpy, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ForeignKey(AImage, on_delete=models.CASCADE,  blank=True, null=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True,null=True)
    roi = models.ForeignKey(ROI, on_delete=models.CASCADE, related_name='transformations')
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE)

    signature = models.CharField(max_length=300,null=True, blank=True)
    objects = TransformationManager()

    def __str__(self):
        return self.name


class Transformer(models.Model):
    path = models.CharField(max_length=500)
    inputmodel = models.CharField(max_length=1000, null=True, blank=True)
    outputmodel = models.CharField(max_length=1000, null=True, blank=True)
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100,null=True, blank=True)
    defaultsettings = models.CharField(max_length=400) #json decoded standardsettings

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.channel)


class Transforming(models.Model):
    transformer = models.ForeignKey(Transformer, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    settings = models.CharField(max_length=1000) # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE,blank=True, null=True)
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    roi = models.ForeignKey(ROI, on_delete=models.CASCADE)

    def __str__(self):
        return "Parsing Request for Filter: {0}".format(self.transformer)