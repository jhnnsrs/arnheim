from django.db import models

# Create your models here.
from elements.models import Sample, Representation
from larvik.models import LarvikConsumer, LarvikJob


class Filter(LarvikConsumer):
    pass

class Filtering(LarvikJob):
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE)
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    pass

