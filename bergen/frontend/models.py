from django.db import models

# Create your models here.


class FrontEndNode(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=500)
    channel = models.CharField(max_length=100, null=True, blank=True)
    inputmodel = models.CharField(max_length=1000, null=True, blank=True)
    outputmodel = models.CharField(max_length=1000, null=True, blank=True)

    defaultsettings = models.CharField(max_length=400) #json decoded standardsettings

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.path)
