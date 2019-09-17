import hashlib
import os
import time

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models

# Create your models here.
from multichat import settings
from representations.models import Experiment


def get_upload_to(instance, filename):
    filename = os.path.join(settings.UPLOAD_PATH, instance.upload_id + '.simg')
    return time.strftime(filename)


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class LargeFile(models.Model):
    ''' a base image upload to hold a file temporarily during upload
            based off of django-chunked-uploads BaseChunkedUpload model
        '''

    file = models.FileField(upload_to=get_upload_to, storage=OverwriteStorage())
    filename = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    size = models.BigIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    def get_label(self):
        return "imagefile"

    def get_abspath(self):
        return os.path.join(settings.MEDIA_ROOT, self.file.name)

    @property
    def md5(self):
        '''calculate the md5 sum of the file'''
        if getattr(self, '_md5', None) is None:
            md5 = hashlib.md5()
            for chunk in self.file.chunks():
                md5.update(chunk)
            self._md5 = md5.hexdigest()
        return self._md5

    def delete(self, delete_file=True, *args, **kwargs):
        '''delete the file and make sure to also delete from storage'''
        if self.file:
            storage, path = self.file.storage, self.file.path
        super(LargeFile, self).delete(*args, **kwargs)
        if self.file and delete_file:
            storage.delete(path)



class Locker(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    location = models.CharField(max_length=1000)


class BioImage(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    file = models.FileField(verbose_name="bioimage",upload_to="bioimagefiles", max_length=1000)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True, null=True, related_name="bioimages")
    locker = models.ForeignKey(Locker,  on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)

        super(BioImage, self).delete(*args, **kwargs)


class BioSeries(models.Model):
    bioimage = models.ForeignKey(BioImage, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True, null=True)
    index = models.IntegerField()
    name = models.CharField(max_length=1000)
    image = models.ImageField(blank=True,null=True)
    isconverted = models.BooleanField()
    nodeid = models.CharField(max_length=300, null=True, blank=True)
    locker = models.ForeignKey(Locker,  on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name




class Analyzer(models.Model):
    path = models.CharField(max_length=500)
    inputmodel = models.CharField(max_length=1000, null=True, blank=True)
    outputmodel = models.CharField(max_length=1000, null=True, blank=True)
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, null=True, blank=True)
    defaultsettings = models.CharField(max_length=400)  # json decoded standardsettings


class Analyzing(models.Model):
    analyzer = models.ForeignKey(Analyzer, on_delete=models.CASCADE, blank=True, null=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True, null=True)
    bioimage = models.ForeignKey(BioImage, on_delete=models.CASCADE)
    nodeid = models.CharField(max_length=300, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    settings = models.CharField(max_length=800)





