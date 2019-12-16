import os

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from elements.models import Experiment, Sample
from bioconverter.models import Representation



class Display(models.Model):
    name = models.CharField(max_length=400, blank=True, null=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, null=True, blank=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    shape = models.CharField(max_length=100, blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="representation_images", blank=True, null=True)

    def delete(self, *args, **kwargs):
        print("Trying to remove Image of path", self.image.path)
        if os.path.isfile(self.image.path):
            os.remove(self.image.path)
            print("Removed Image of path", self.image.path)

        super(Display, self).delete(*args, **kwargs)


class Exhibit(models.Model):
    name = models.CharField(max_length=400, blank=True, null=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, null=True, blank=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    shape = models.CharField(max_length=100, blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE, blank=True, null=True)
    niftipath = models.FileField(upload_to="nifti",blank=True, null=True)

    def delete(self, *args, **kwargs):
        print("Trying to remove Nifti of path", self.niftipath.path)
        if os.path.isfile(self.niftipath.path):
            os.remove(self.niftipath.path)
            print("Removed Nifti of path", self.niftipath.path)

        super(Exhibit, self).delete(*args, **kwargs)


class Metamorpher(models.Model):
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100) # not the colour but the django channel
    defaultsettings = models.CharField(max_length=400) #json decoded standardsettings

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.channel)




class Metamorphing(models.Model):

    nodeid = models.CharField(max_length=400, null=True, blank=True)
    metamorpher = models.ForeignKey(Metamorpher, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    settings = models.CharField(max_length=1000) # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    # The inputvid will pe parsed to the outputmodel (if no representation in that slot exists it will be created
    # otherwise just updated# the requested model which ought to be converted
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "ConversionRequest for Converter: {0}".format(self.metamorpher)




