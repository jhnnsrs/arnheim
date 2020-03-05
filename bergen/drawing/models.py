# Create your models here.
from django.db import models

from elements.models import ROI


class LineROI(ROI):
    length = models.IntegerField(blank=True, null=True)