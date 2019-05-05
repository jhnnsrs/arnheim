import os

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from biouploader.models import BioImage, BioSeries
from drawing.models import Sample
from representations.models import Experiment


class BioImageFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(verbose_name="bioimage",upload_to="bioimagefiles")
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name="bioimagefiles", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)

        super(BioImageFile, self).delete(*args, **kwargs)


class Converter(models.Model):
    path = models.CharField(max_length=500)
    inputmodel = models.CharField(max_length=1000, null=True, blank=True)
    outputmodel = models.CharField(max_length=1000, null=True, blank=True)
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, null=True, blank=True)
    defaultsettings = models.CharField(max_length=400)  # json decoded standardsettings

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.path)


class ConversionRequest(models.Model):
    converter = models.ForeignKey(Converter, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    settings = models.CharField(max_length=1000) # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    nodeid = models.CharField(max_length=300, null=True, blank=True)
    # The inputvid will pe parsed to the output vid (if no representation in that slot exists it will be created
    # otherwise just updated
    bioimage = models.ForeignKey(BioImage, on_delete=models.CASCADE)# the requested model which ought to be converted
    outputvid = models.IntegerField()
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True, null= True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "ConversionRequest for Converter: {0}".format(self.converter)

class Conversing(models.Model):
    override = models.BooleanField()
    converter = models.ForeignKey(Converter, on_delete=models.CASCADE)
    bioserie = models.ForeignKey(BioSeries, on_delete=models.CASCADE)
    settings = models.CharField(max_length=1000) # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    nodeid = models.CharField(max_length=300, null=True, blank=True)
    # The inputvid will pe parsed to the output vid (if no representation in that slot exists it will be created
    # otherwise just updated
    outputvid = models.IntegerField()
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True, null= True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "ConversionRequest for Converter: {0}".format(self.converter)

class ConvertToSampleRequest(models.Model):
    converter = models.ForeignKey(Converter, on_delete=models.CASCADE)

    # SAMPLE PROPERTIES FOR CREATION
    location = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True, null=True)

    settings = models.CharField(max_length=1000) # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    # The inputvid will pe parsed to the output vid (if no representation in that slot exists it will be created
    # otherwise just updated
    bioimage = models.ForeignKey(BioImage, on_delete=models.CASCADE) # the requested model which ought to be converted
    outputvid = models.IntegerField()

    def __str__(self):
        return "ConversionRequest for Converter: {0}".format(self.converter)



class JobRequest(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)