from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from drawing.models import Sample
from filterbank.models import Representation, Nifti, AImage
from representations.models import Experiment


class Display(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, null=True, blank=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    shape = models.CharField(max_length=100, blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="representation_images", blank=True, null=True)


class Exhibit(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, null=True, blank=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    shape = models.CharField(max_length=100, blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE, blank=True, null=True)
    nifti = models.ForeignKey(Nifti, on_delete=models.CASCADE, blank=True, null=True)
    niftipath = models.FileField(upload_to="nifti",blank=True, null=True)


class Test(models.Model):
    name = models.CharField(max_length=100)

class Metamorpher(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=500)
    outputtype = models.CharField(max_length=200) #should contain a list of the model it can convert
    channel = models.CharField(max_length=100) # not the colour but the django channel
    defaultsettings = models.CharField(max_length=400) #json decoded standardsettings

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.path)




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