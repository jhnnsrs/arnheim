import os
import uuid

from django.contrib.auth.models import User
from django.db import models

from elements.models import Experiment
# Create your models here.
from elements.models import Sample
from larvik.logging import get_module_logger
from larvik.models import LarvikConsumer, LarvikJob

# Create your models here.

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
    nodeid = models.CharField(max_length=2000)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        logger.info("Trying to remove Bioimage of path {0}".format(self.file.path))
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)
            logger.info("Removed Bioimage of path {0}".format(self.file.path))

        super(BioImage, self).delete(*args, **kwargs)


class BioSeries(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, null=True, blank=True, related_name="bioseries")
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




class Analyzer(LarvikConsumer):
    def __str__(self):
        return f"Analyzer {self.name}"


class Analyzing(LarvikJob):
    analyzer = models.ForeignKey(Analyzer, on_delete=models.CASCADE, blank=True, null=True)
    bioimage = models.ForeignKey(BioImage, on_delete=models.CASCADE)



class Converter(LarvikConsumer):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{0} at Channel {1}".format(self.name, self.channel)


class Conversing(LarvikJob):
    converter = models.ForeignKey(Converter, on_delete=models.CASCADE)
    bioserie = models.ForeignKey(BioSeries, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True, null= True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "ConversionRequest for Converter: {0}".format(self.converter)


