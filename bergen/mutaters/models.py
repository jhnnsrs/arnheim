from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from drawing.models import Sample, ROI
from filterbank.models import Nifti
from representations.models import Experiment
from transformers.models import Transformation

class Reflection(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, null=True, blank=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    roi = models.ForeignKey(ROI, on_delete=models.CASCADE, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    shape = models.CharField(max_length=100, blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    transformation = models.ForeignKey(Transformation, on_delete=models.CASCADE, blank=True, null=True)
    nifti = models.ForeignKey(Nifti, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="transformation_images", blank=True, null=True)


class Mutater(models.Model):
    path = models.CharField(max_length=500)
    inputmodel = models.CharField(max_length=1000, null=True, blank=True)
    outputmodel = models.CharField(max_length=1000, null=True, blank=True)
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, null=True, blank=True)
    defaultsettings = models.CharField(max_length=400)  # json decoded standardsettings

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.path)


class Mutating(models.Model):
    mutater = models.ForeignKey(Mutater, on_delete=models.CASCADE)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    settings = models.CharField(max_length=1000) # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    transformation = models.ForeignKey(Transformation, on_delete=models.CASCADE, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "Mutating for Converter: {0}".format(self.mutator)