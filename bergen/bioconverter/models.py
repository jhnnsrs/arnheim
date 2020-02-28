import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.template.loader import render_to_string

from bioconverter.managers import DistributedRepresentationManager, RepresentationManager
from biouploader.models import BioSeries
from elements.models import Experiment, Sample, Zarr
from larvik.models import LarvikConsumer, LarvikJob, LarvikArrayProxy


class Converter(LarvikConsumer):
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, unique=True, default=uuid.uuid4())
    defaultsettings = models.CharField(max_length=1000)  # json decoded standardsettings

    def __str__(self):
        return "{0} at Channel {1}".format(self.name, self.channel)


class Conversing(LarvikJob):
    converter = models.ForeignKey(Converter, on_delete=models.CASCADE)
    bioserie = models.ForeignKey(BioSeries, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True, null= True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "ConversionRequest for Converter: {0}".format(self.converter)


class Representation(LarvikArrayProxy):
    name = models.CharField(max_length=1000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    vid = models.CharField(max_length=1000,blank=True, null=True) #deprecated
    inputrep = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null= True)
    shape = models.CharField(max_length=100, blank=True, null= True) #deprecated
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE,related_name='representations')
    zarr: Zarr = models.ForeignKey(Zarr, on_delete=models.CASCADE, blank=True, null=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=400, blank=True, null=True)
    chain = models.CharField(max_length=9000, blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    meta = models.CharField(max_length=6000, null=True, blank=True) #deprecated

    objects = RepresentationManager()
    distributed = DistributedRepresentationManager()

    def __str__(self):
        return self.name

    def _repr_html_(self):
        return f"<h3>{self.name}</h3><ul><li>Sample Name: {self.sample.name}</li></ul>"

    def delete(self, *args, **kwargs):
        if self.zarr:
            self.zarr.delete()

        super(Representation, self).delete(*args, **kwargs)
