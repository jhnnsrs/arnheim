import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class LarvikJob(models.Model):
    statuscode = models.IntegerField( null=True, blank=True)
    statusmessage = models.CharField(max_length=500,  null=True, blank=True)
    settings = models.CharField(max_length=1000) # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    nodeid = models.CharField(max_length=400, null=True, blank=True)

    class Meta:
        abstract = True

    def _repr_html_(self):
        return f'''<h5>Request by {self.creator.username} </h5>
                <ul>
                    <li> Last Status: {self.statusmessage}</li>
                    <li> Node Status: {self.nodeid}</li>
                    <li> Settings: {self.settings}</li>
                </ul>'''

class LarvikConsumer(models.Model):
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, unique=True, default=uuid.uuid4())
    settings = models.CharField(max_length=1000)  # json decoded standardsettings

    class Meta:
        abstract = True




class LarvikArrayProxy(models.Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getattr__(self, item):
        return getattr(self.array, item)

    class Meta:
        abstract = True

    @property
    def array(self):
        if self.zarr:
            return self.zarr.openArray(chunks="auto", name="data")


