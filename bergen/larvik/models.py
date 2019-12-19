from django.db import models

# Create your models here.
class LarvikJob(models.Model):
    statuscode = models.IntegerField()
    statusmessage = models.CharField(max_length=500)