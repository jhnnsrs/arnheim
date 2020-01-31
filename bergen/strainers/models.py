from django.db import models

# Create your models here.
from elements.models import Experiment, Sample
from larvik.models import LarvikConsumer, LarvikJob
from transformers.models import Transformation


class Strainer(LarvikConsumer):

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.channel)


class Straining(LarvikJob):
    strainer = models.ForeignKey(Strainer, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE,blank=True, null=True)
    transformation = models.ForeignKey(Transformation, on_delete=models.CASCADE)


    def __str__(self):
        return "Parsing Request for Filter: {0}".format(self.strainer)


