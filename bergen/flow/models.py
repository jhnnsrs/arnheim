from django.contrib.auth.models import User, Group
from django.db import models

# Create your models here.


class Flow(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True, default="Not Set")
    diagram = models.CharField(max_length=50000)
    description = models.CharField(max_length=50000, default="Add a Description")


class Node(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    entityid = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)
    nodeclass = models.CharField(max_length=300, default="classic-node")
    path = models.CharField(max_length=500)
    channel = models.CharField(max_length=100, null=True, blank=True)
    inputmodel = models.CharField(max_length=1000, null=True, blank=True)
    outputmodel = models.CharField(max_length=1000, null=True, blank=True)

    defaultsettings = models.CharField(max_length=5000) #json decoded standardsettings

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.path)


class ForeignNodeRequest(models.Model):
    nodeid = models.CharField(max_length=100)
    origin = models.CharField(max_length=300)
    data = models.TextField()

class ForeignNodeStatus(models.Model):
    nodeid = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=200)
    creator = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)

class Layout(models.Model):
    name = models.CharField(max_length=100)
    layout = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    flows = models.ManyToManyField(Flow)