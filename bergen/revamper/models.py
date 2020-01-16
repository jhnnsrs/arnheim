from django.db import models
# Create your models here.
from registration.forms import User

from elements.models import Experiment, Sample
from transformers.models import Transformation


class Mask(models.Model):
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "masks")
    vectors = models.CharField(max_length=3000)
    color = models.CharField(max_length=100, blank=True, null=True)
    signature = models.CharField(max_length=300,null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    sample = models.ForeignKey(Sample,on_delete=models.CASCADE, related_name= "masks")
    transformation = models.ForeignKey(Transformation, on_delete=models.CASCADE,blank=True, null=True, related_name= "masks")
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True,null=True, related_name= "masks")

    def __str__(self):
        return "Mask Creator at {0} on Transformation {1}".format(self.created_at.timestamp(),self.transformation.name)


class Revamper(models.Model):
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, null=True, blank=True)
    defaultsettings = models.CharField(max_length=400)  # json decoded standardsettings

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.channel)


class Revamping(models.Model):
    revamper = models.ForeignKey(Revamper, on_delete=models.CASCADE)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    settings = models.CharField(max_length=1000) # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    transformation = models.ForeignKey(Transformation, on_delete=models.CASCADE, blank=True, null=True)
    mask = models.ForeignKey(Mask, on_delete=models.CASCADE, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "Revamping for Revamper: {0}".format(self.revamper)


