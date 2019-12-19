from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from biouploader.models import Locker


class Importer(models.Model):
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, null=True, blank=True)
    defaultsettings = models.CharField(max_length=400)  # json decoded standardsettings

    def __str__(self):
        return "{0} at Channel {1}".format(self.name, self.channel)

class Job(models.Model):
    statuscode = models.IntegerField()
    statusmessage = models.CharField(max_length=500)


class Importing(models.Model):
    importer = models.ForeignKey(Importer, on_delete=models.CASCADE)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    override = models.BooleanField()
    settings = models.CharField(max_length=1000)  # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    locker = models.ForeignKey(Locker, on_delete=models.SET_NULL, null=True, blank=True)
    error = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return "Importing for Importer {1} created at {0}".format(self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),self.importer.name)