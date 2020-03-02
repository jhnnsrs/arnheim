from django.contrib.auth.models import User
from django.db import models

from elements.models import Experiment, Sample, Representation, Transformation, ROI
from larvik.models import LarvikConsumer, LarvikJob


# Create your models here.

class Evaluator(LarvikConsumer):
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, null=True, blank=True)
    defaultsettings = models.CharField(max_length=400)  # json decoded standardsettings

    def __str__(self):
        return "{0} at Channel {1}".format(self.name, self.channel)


class Evaluating(LarvikJob):
    evaluator = models.ForeignKey(Evaluator, on_delete=models.CASCADE)
    override = models.BooleanField()
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE,blank=True, null=True)
    transformation = models.ForeignKey(Transformation, on_delete=models.CASCADE)
    roi = models.ForeignKey(ROI, on_delete=models.CASCADE)

    def __str__(self):
        return "Evaluating for Evaluator: {0}".format(self.evaluator)

class Data(models.Model):

    signature = models.CharField(max_length=300, null=True, blank=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    vid = models.CharField(max_length=300)
    name = models.CharField(max_length=4000)
    type = models.CharField(max_length=100) #includes the type of data generations
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='datas')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True,null=True)
    roi = models.ForeignKey(ROI, on_delete=models.CASCADE, related_name='datas',blank=True, null=True)
    transformation = models.ForeignKey(Transformation, on_delete=models.CASCADE, related_name='datas',blank=True, null=True)
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE, blank=True, null=True)
    evaluating = models.ForeignKey(Evaluating, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

class VolumeData(Data):
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


class LengthData(Data):
    pixellength = models.IntegerField()
    physicallength = models.FloatField()
    distancetostart = models.IntegerField()
    physicaldistancetostart = models.FloatField()
    distancetoend = models.IntegerField()
    physicaldistancetoend = models.FloatField()


class ClusterData(Data):
    clusternumber = models.IntegerField()
    clusterareapixels = models.IntegerField()
    clusterarea = models.FloatField()

