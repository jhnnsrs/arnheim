from django.db import models

# Create your models here.
from bioconverter.models import Locker
from larvik.models import LarvikConsumer, LarvikJob


class Importer(LarvikConsumer):
    def __str__(self):
        return "{0} at Channel {1}".format(self.name, self.channel)


class Importing(LarvikJob):
    importer = models.ForeignKey(Importer, on_delete=models.CASCADE)
    locker = models.ForeignKey(Locker, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "Importing for Importer {0} ".format(self.importer.name)
