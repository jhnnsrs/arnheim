from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from elements.models import Experiment, Sample, Transformation, ROI
from larvik.models import LarvikConsumer, LarvikJob
from mutaters.managers import ReflectionManager


class Reflection(models.Model):
    name = models.CharField(max_length=300)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    shape = models.CharField(max_length=100, blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    transformation = models.ForeignKey(Transformation, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="transformation_images", blank=True, null=True)

    objects = ReflectionManager()

    def delete(self,*args,**kwargs):
        self.image.delete()

        super(Reflection, self).delete(*args,**kwargs)


class Mutater(LarvikConsumer):

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.channel)


class Mutating(LarvikJob):
    mutater = models.ForeignKey(Mutater, on_delete=models.CASCADE)
    transformation = models.ForeignKey(Transformation, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "Mutating for Mutater: {0}".format(self.mutater.name)