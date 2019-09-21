from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from bioconverter.managers import RepresentationManager
from biouploader.models import BioSeries
from elements.models import Experiment, Sample, Numpy

class Converter(models.Model):
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, null=True, blank=True)
    defaultsettings = models.CharField(max_length=1000)  # json decoded standardsettings

    def __str__(self):
        return "{0} at Channel {1}".format(self.name, self.channel)


class Conversing(models.Model):
    converter = models.ForeignKey(Converter, on_delete=models.CASCADE)
    bioserie = models.ForeignKey(BioSeries, on_delete=models.CASCADE)
    settings = models.CharField(max_length=1000) # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    nodeid = models.CharField(max_length=300, null=True, blank=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True, null= True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "ConversionRequest for Converter: {0}".format(self.converter)


class Representation(models.Model):
    name = models.CharField(max_length=1000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    vid = models.CharField(max_length=1000,blank=True, null=True)
    inputrep = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null= True)
    shape = models.CharField(max_length=100, blank=True, null= True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE,related_name='representations')
    numpy = models.ForeignKey(Numpy, on_delete=models.CASCADE, blank=True, null=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    meta = models.CharField(max_length=6000, null=True, blank=True)

    objects = RepresentationManager()

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.numpy:
            self.numpy.delete()

        super(Representation, self).delete(*args, **kwargs)


