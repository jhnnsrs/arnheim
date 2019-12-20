import os

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from larvik.logging import get_module_logger

logger = get_module_logger(__name__)

class Locker(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    location = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class BioImage(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    file = models.FileField(verbose_name="bioimage",upload_to="bioimages", max_length=1000)
    locker = models.ForeignKey(Locker,  on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        logger.info("Trying to remove Bioimage of path {0}".format(self.file.path))
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)
            logger.info("Removed Bioimage of path {0}".format(self.file.path))

        super(BioImage, self).delete(*args, **kwargs)


class BioSeries(models.Model):
    bioimage = models.ForeignKey(BioImage, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
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
    bioimage = models.ForeignKey(BioImage, on_delete=models.CASCADE)
    nodeid = models.CharField(max_length=300, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    settings = models.CharField(max_length=800)

    statuscode = models.IntegerField(blank=True, null=True)
    statusmessage = models.CharField(max_length=500, blank=True, null=True)


class BioMeta(models.Model):
    json = models.CharField(max_length=2000, blank=True, null=True)
    channellist = models.CharField(max_length=2000)
    xresolution = models.IntegerField()
    yresolution = models.IntegerField()
    cresolution = models.IntegerField()
    zresolution = models.IntegerField()
    tresolution = models.IntegerField()

    xphysical = models.FloatField()
    yphysical = models.FloatField()
    zphysical = models.FloatField()
    spacial_units = models.CharField(max_length=30)
    temporal_units = models.CharField(max_length=30)
    seriesname = models.CharField(max_length=100, blank=True,null=True)