from django.contrib.auth.models import User
from django.db import models

from drawing.models import ROI
# Create your models here.
from elements.models import Experiment, Sample
from larvik.models import LarvikConsumer, LarvikJob
from transformers.models import Transformation


class Reflection(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, null=True, blank=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    roi = models.ForeignKey(ROI, on_delete=models.CASCADE, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    shape = models.CharField(max_length=100, blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    transformation = models.ForeignKey(Transformation, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="transformation_images", blank=True, null=True)

    def delete(self,*args,**kwargs):
        self.image.delete()

        super(Reflection, self).delete(*args,**kwargs)


class Mutater(LarvikConsumer):

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.channel)


class Mutating(LarvikJob):
    mutater = models.ForeignKey(Mutater, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    transformation = models.ForeignKey(Transformation, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "Mutating for Mutater: {0}".format(self.mutater.name)