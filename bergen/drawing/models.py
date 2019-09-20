# Create your models here.
from django.contrib.auth.models import User
from django.db import models

from bioconverter.models import Representation
from elements.models import Sample, Experiment
from metamorphers.models import Display


class ROI(models.Model):

    nodeid = models.CharField(max_length=400, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    vectors = models.CharField(max_length=3000)
    color = models.CharField(max_length=100, blank=True, null=True)
    signature = models.CharField(max_length=300,null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    sample = models.ForeignKey(Sample,on_delete=models.CASCADE,blank=True, null=True)
    display = models.ForeignKey(Display,on_delete=models.CASCADE,blank=True, null=True)
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE,blank=True, null=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True,null=True)

    def __str__(self):
        return "ROI created at {0} on Sample {1}".format(self.created_at.timestamp(),self.sample.name)