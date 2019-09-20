import os

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models

# Create your models here.
from bioconverter.models import Representation
from elements.models import Experiment, Sample
from multichat import settings


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name):
        """Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name



class Filter(models.Model):
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, null=True, blank=True)

    defaultsettings = models.CharField(max_length=400) #json decoded standardsettings

    def __str__(self):
        return "{0} at Channel {1}".format(self.name, self.channel)


class Filtering(models.Model):
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE)
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    settings = models.CharField(max_length=1000) # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE,blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)




