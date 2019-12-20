import os

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from elements.models import Experiment, Sample
from drawing.models import ROI
from transformers.models import Transformation

class Reflection(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, null=True, blank=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    roi = models.ForeignKey(ROI, on_delete=models.CASCADE, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    shape = models.CharField(max_length=100, blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    transformation = models.ForeignKey(Transformation, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="transformation_images", blank=True, null=True)

    def delete(self,*args,**kwargs):
        self.image.delete()

        super(Reflection, self).delete(*args,**kwargs)


class Mutater(models.Model):
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, null=True, blank=True)
    defaultsettings = models.CharField(max_length=400)  # json decoded standardsettings

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.channel)


class Mutating(models.Model):
    mutater = models.ForeignKey(Mutater, on_delete=models.CASCADE)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    settings = models.CharField(max_length=1000) # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    transformation = models.ForeignKey(Transformation, on_delete=models.CASCADE, blank=True, null=True)
    statuscode = models.IntegerField(blank=True, null=True)
    statusmessage = models.CharField(max_length=500, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "Mutating for Mutater: {0}".format(self.mutater.name)