import os

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from elements.models import Experiment, Sample, Representation
from larvik.models import LarvikJob, LarvikConsumer
from metamorphers.managers import DisplayManager


class Display(models.Model):
    name = models.CharField(max_length=400, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    shape = models.CharField(max_length=100, blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="representation_images", blank=True, null=True)

    objects = DisplayManager()

    def delete(self, *args, **kwargs):
        print("Trying to remove Image of path", self.image.path)
        if os.path.isfile(self.image.path):
            os.remove(self.image.path)
            print("Removed Image of path", self.image.path)

        super(Display, self).delete(*args, **kwargs)


class Exhibit(models.Model):
    name = models.CharField(max_length=400, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    shape = models.CharField(max_length=100, blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE, blank=True, null=True)
    niftipath = models.FileField(upload_to="nifti",blank=True, null=True)

    def delete(self, *args, **kwargs):
        print("Trying to remove Nifti of path", self.niftipath.path)
        if os.path.isfile(self.niftipath.path):
            os.remove(self.niftipath.path)
            print("Removed Nifti of path", self.niftipath.path)

        super(Exhibit, self).delete(*args, **kwargs)


class Metamorpher(LarvikConsumer):

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.channel)




class Metamorphing(LarvikJob):
    metamorpher = models.ForeignKey(Metamorpher, on_delete=models.CASCADE)
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return "Metamorphing for Metamorpher: {0}".format(self.metamorpher)




