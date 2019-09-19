from django.contrib.auth.models import User
from django.db import models
import os

import h5py

from biouploader.models import BioSeries
from multichat import settings

# Create your models here.
from representations.models import Experiment

class BioMeta(models.Model):
    json = models.CharField(max_length=2000, blank=True, null=True)
    channellist = models.CharField(max_length=2000)
    xresolution = models.IntegerField()
    yresolution = models.IntegerField()
    cresolution = models.IntegerField()
    zresolution = models.IntegerField()
    tresolution = models.IntegerField()

    xphysical = models.FloatField()
    yphysical = models.FloatField()
    zphysical = models.FloatField()
    spacial_units = models.CharField(max_length=30)
    temporal_units = models.CharField(max_length=30)
    seriesname = models.CharField(max_length=100, blank=True,null=True)



class Sample(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=400)
    name = models.CharField(max_length=1000)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True, null=True)
    bioseries = models.ForeignKey(BioSeries, on_delete=models.CASCADE, blank=True, null=True)
    meta = models.ForeignKey(BioMeta, on_delete=models.CASCADE, blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)


    def __str__(self):
        return "{0} by User: {1}".format(self.name,self.creator.username)



from filterbank.models import Representation

class ROI(models.Model):

    nodeid = models.CharField(max_length=400, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    vectors = models.CharField(max_length=3000)
    color = models.CharField(max_length=100, blank=True, null=True)
    signature = models.CharField(max_length=300,null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    sample = models.ForeignKey(Sample,on_delete=models.CASCADE)
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE,blank=True, null=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True,null=True)

    def __str__(self):
        return "ROI created at {0} on Sample {1}".format(self.created_at.timestamp(),self.sample.name)