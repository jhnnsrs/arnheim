from django.db import models


class Job(models.Model):
    statuscode = models.IntegerField()
    statusmessage = models.CharField(max_length=500)