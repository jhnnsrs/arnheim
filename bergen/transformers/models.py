from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from elements.models import Experiment, Sample, Numpy
from drawing.models import ROI
from bioconverter.models import Representation
from transformers.managers import TransformationManager


class Transformation(models.Model):
    name = models.CharField(max_length=1000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    vid = models.CharField(max_length=200)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    shape = models.CharField(max_length=100, blank=True, null= True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='transformations')
    numpy = models.ForeignKey(Numpy, on_delete=models.CASCADE, blank=True, null=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True,null=True)
    roi = models.ForeignKey(ROI, on_delete=models.CASCADE, related_name='transformations')
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE)

    signature = models.CharField(max_length=300,null=True, blank=True)
    objects = TransformationManager()

    def __str__(self):
        return self.name


class Transformer(models.Model):
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


