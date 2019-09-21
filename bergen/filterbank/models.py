import os

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models

# Create your models here.
from bioconverter.models import Representation
from elements.models import Experiment, Sample
from mandal import settings


class Filter(models.Model):
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, null=True, blank=True)

    defaultsettings = models.CharField(max_length=400) #json decoded standardsettings

    def __str__(self):
        return "{0} at Channel {1}".format(self.name, self.channel)


class Filtering(models.Model):
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE)
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    settings = models.CharField(max_length=1000) # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE,blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return "{1} of {0} on Sample {2}".format(self.representation.name, self.filter.name, self.sample.name)




