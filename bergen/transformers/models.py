from django.db import models

# Create your models here.
from elements.models import Experiment, Sample, Representation, ROI
from larvik.models import LarvikConsumer, LarvikJob


class Transformer(LarvikConsumer):

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.channel)


class Transforming(LarvikJob):
    transformer = models.ForeignKey(Transformer, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE,blank=True, null=True)
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE)
    roi = models.ForeignKey(ROI, on_delete=models.CASCADE)


    def __str__(self):
        return "Parsing Request for Filter: {0}".format(self.transformer)


