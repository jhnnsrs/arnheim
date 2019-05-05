from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from taggit.managers import TaggableManager

from drawing.models import Sample, ROI, BioMeta
from representations.models import Experiment
from transformers.models import Transformation


class Data(models.Model):

    signature = models.CharField(max_length=300, null=True, blank=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    vid = models.CharField(max_length=300)
    name = models.CharField(max_length=100)
    items = models.CharField(max_length=600) # jsondecoded?
    type = models.CharField(max_length=100) #includes the type of data generations
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='datas')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True,null=True)
    roi = models.ForeignKey(ROI, on_delete=models.CASCADE, related_name='datas')
    transformation = models.ForeignKey(Transformation, on_delete=models.CASCADE, related_name='datas')
    tags = TaggableManager()

    def __str__(self):
        return self.name

class VolumeData(Data):
    meta = models.ForeignKey(BioMeta, on_delete=models.CASCADE)
    b4channel = models.IntegerField()
    aisstart = models.IntegerField()
    aisend = models.IntegerField()
    pixellength = models.IntegerField()
    physicallength = models.FloatField()
    vectorlength = models.FloatField()
    diameter = models.IntegerField()
    threshold = models.FloatField()
    userdefinedstart= models.IntegerField()
    userdefinedend = models.IntegerField()
    intensitycurves = models.CharField(max_length=5000)




class Evaluator(models.Model):
    path = models.CharField(max_length=500)
    inputmodel = models.CharField(max_length=1000, null=True, blank=True)
    outputmodel = models.CharField(max_length=1000, null=True, blank=True)
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, null=True, blank=True)
    defaultsettings = models.CharField(max_length=400)  # json decoded standardsettings

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.channel)


class Evaluating(models.Model):
    evaluator = models.ForeignKey(Evaluator, on_delete=models.CASCADE)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    override = models.BooleanField()
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    settings = models.CharField(max_length=1000) # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE,blank=True, null=True)
    transformation = models.ForeignKey(Transformation, on_delete=models.CASCADE)
    roi = models.ForeignKey(ROI, on_delete=models.CASCADE)
    error = models.CharField(max_length=300,blank=True,null=True)

    def __str__(self):
        return "Evaluating for Evaluator: {0}".format(self.evaluator)