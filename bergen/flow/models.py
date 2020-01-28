import uuid

from django.contrib.auth.models import User, Group
from django.db import models


# Create your models here.
from larvik.discover import createUniqeNodeName


class Flow(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True, default="Not Set")
    diagram = models.CharField(max_length=50000)
    description = models.CharField(max_length=50000, default="Add a Description")


class Node(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    entityid = models.IntegerField(null=True, blank=True)
    hash = models.CharField(max_length=300, default=createUniqeNodeName, unique=True)
    variety = models.CharField(max_length=100,  null=True, blank=True)
    name = models.CharField(max_length=100)
    nodeclass = models.CharField(max_length=300, default="classic-node")
    path = models.CharField(max_length=500)
    channel = models.CharField(max_length=100, null=True, blank=True)
    inputmodel = models.CharField(max_length=1000, null=True, blank=True)
    outputmodel = models.CharField(max_length=1000, null=True, blank=True)

    defaultsettings = models.CharField(max_length=5000) #json decoded standardsettings

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.path)


class External(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    uniqueid = models.CharField(max_length=400, unique=True, blank=True, null=True)
    node = models.CharField(max_length=2000) #The Nodepath for instantiating
    defaultsettings = models.CharField(max_length=2000) #The DefaultSettings
    origin = models.CharField(max_length=2000) #The DefaultSettings
    links = models.CharField(max_length=6000) #All of the Links of that Diagram
    ports = models.CharField(max_length=7000 ,null=True, blank=True)
    status = models.CharField(max_length=200) #Is Alive #is not Alive
    graphname = models.CharField(max_length=200) #Is Alive #is not Alive
    creator = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)


class ExternalRequest(models.Model):
    external = models.ForeignKey(External, on_delete=models.CASCADE) # The external thing it should deliver to
    data = models.CharField(max_length=6000) # The Model that is being send
    port = models.CharField(max_length=2000) # The Port for its delivery
    instance = models.CharField(max_length=2000) #the instance name of
    model = models.CharField(max_length=200) #The Model Type eg Representation
    origin = models.CharField(max_length=400) #The Origin of the request (UUID of the Window)
    kind = models.CharField(max_length=100) # if in or out or what
    created_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class Layout(models.Model):
    name = models.CharField(max_length=100)
    layout = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    flows = models.ManyToManyField(Flow)