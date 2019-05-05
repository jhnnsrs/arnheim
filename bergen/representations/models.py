import h5py
from django.contrib.auth.models import User
from django.db import models

from taggit.managers import TaggableManager
# Create your models here.

class Experiment(models.Model):
    name = models.CharField(max_length=200)
    tags = TaggableManager()
    description = models.CharField(max_length=1000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return "Experiment {0} by {1}".format(self.name,self.creator.username)
