from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from elements.models import Experiment, Sample
from transformers.models import Transformation


class Strainer(models.Model):
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100,null=True, blank=True)
    defaultsettings = models.CharField(max_length=400) #json decoded standardsettings

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.channel)


class Straining(models.Model):
    strainer = models.ForeignKey(Strainer, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    settings = models.CharField(max_length=1000) # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE,blank=True, null=True)
    transformation = models.ForeignKey(Transformation, on_delete=models.CASCADE)
    nodeid = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return "Parsing Request for Filter: {0}".format(self.strainer)


