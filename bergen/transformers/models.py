from django.contrib.auth.models import User
from django.db import models

from bioconverter.models import Representation
from drawing.models import ROI
# Create your models here.
from elements.models import Experiment, Sample,Zarr
from larvik.models import LarvikConsumer, LarvikJob
from transformers.managers import TransformationManager, DistributedTransformationManager


class Transformation(models.Model):
    name = models.CharField(max_length=1000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    vid = models.CharField(max_length=200)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    shape = models.CharField(max_length=100, blank=True, null= True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='transformations')
    zarr = models.ForeignKey(Zarr, on_delete=models.CASCADE, blank=True, null=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True,null=True)
    roi = models.ForeignKey(ROI, on_delete=models.CASCADE, related_name='transformations')
    representation = models.ForeignKey(Representation, on_delete=models.SET_NULL, blank=True, null=True)
    inputtransformation = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null= True)

    signature = models.CharField(max_length=300,null=True, blank=True)
    objects = TransformationManager()
    distributed = DistributedTransformationManager()

    def loadArray(self, chunks="auto", name="data"):
        if self.zarr:
            return self.zarr.openArray(chunks= chunks, name=name)
        if self.numpy:
            return self.numpy.get_array()


    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.numpy:
            self.numpy.delete()
        if self.zarr:
            self.zarr.delete()

        super(Transformation, self).delete(*args, **kwargs)


class Transformer(LarvikConsumer):

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.channel)


class Transforming(LarvikJob):
    transformer = models.ForeignKey(Transformer, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE,blank=True, null=True)
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE)
    roi = models.ForeignKey(ROI, on_delete=models.CASCADE)


    def __str__(self):
        return "Parsing Request for Filter: {0}".format(self.transformer)


