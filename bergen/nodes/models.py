from django.contrib.auth.models import User
from django.db import models



# Create your models here.
from mutaters.models import Mutater


class ArnheimHost(models.Model):
    type = models.CharField(max_length=100) # e.g. Local / Foreign
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200) # eg. Uni-Heidelberg Arnheim Server
    rooturl = models.CharField(max_length=100) # e.g http://johannesroos.de/
    token = models.CharField(max_length=100,null=True,blank=True) #e.g oauth token for endpoint
    expiry_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.name



class NodeVariety(models.Model):
    type = models.CharField(max_length=400)
    host = models.ForeignKey(ArnheimHost, on_delete=models.CASCADE) # e.g the ArnheimLocation
    url = models.CharField(max_length=200) # e.g. the link /filters/
    parser = models.CharField(max_length=100) # e.g the link where parsing requests are pushed to
    name = models.CharField(max_length=400) # e.g Filters

    def __str__(self):
        return self.name



class NodeElement(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    variety = models.ForeignKey(NodeVariety, on_delete=models.CASCADE)
    entity = models.IntegerField()

class Node(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    entityid = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)
    variety = models.ForeignKey(NodeVariety, on_delete=models.CASCADE)
    nodeclass = models.CharField(max_length=300, default="classic-node")
    path = models.CharField(max_length=500)
    channel = models.CharField(max_length=100, null=True, blank=True)
    inputmodel = models.CharField(max_length=1000, null=True, blank=True)
    outputmodel = models.CharField(max_length=1000, null=True, blank=True)

    defaultsettings = models.CharField(max_length=5000) #json decoded standardsettings

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.path)