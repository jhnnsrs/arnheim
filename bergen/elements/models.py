import h5py
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from taggit.managers import TaggableManager

from biouploader.models import BioSeries, BioMeta
from elements.managers import NumpyManager


class Antibody(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}".format(self.name)


class Experiment(models.Model):
    name = models.CharField(max_length=200)
    tags = TaggableManager()
    description = models.CharField(max_length=1000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return "Experiment {0} by {1}".format(self.name,self.creator.username)


class Sample(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=400)
    name = models.CharField(max_length=1000)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True, null=True)
    bioseries = models.ForeignKey(BioSeries, on_delete=models.CASCADE, blank=True, null=True)
    meta = models.ForeignKey(BioMeta, on_delete=models.CASCADE, blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)


    def __str__(self):
        return "{0} by User: {1}".format(self.name,self.creator.username)


class Numpy(models.Model):
    filepath = models.FilePathField(max_length=400) # aka h5files/$sampleid.h5
    vid = models.CharField(max_length=1000) # aca vid0, vid1, vid2, vid3
    type = models.CharField(max_length=100)
    dtype = models.CharField(max_length=300, blank=True, null=True)
    compression = models.CharField(max_length=300, blank=True, null=True)
    shape = models.CharField(max_length=400, blank=True, null=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    # Custom Manager to simply create an array
    objects = NumpyManager()

    def get_array(self):
        with h5py.File(self.filepath, 'a') as file:
            print("Trying to access file {0} to get array".format(self.filepath))
            hf = file[self.type]
            array = hf.get(self.vid)[()]
        return array

    def set_array(self,array):
        with h5py.File(self.filepath, 'a') as file:
            print("Trying to access file {0} to set array".format(self.filepath))
            hf = file[self.type]
            if self.vid in hf: del hf[self.vid]
            hf.create_dataset(self.vid, data=array, dtype=self.dtype, compression=self.compression)

    def get_z_bounded_array(self,zl,zu):
        with h5py.File(self.filepath, "a") as file:
            print("Trying to access file {0} to set array".format(self.filepath))
            hf = file[self.type]
            ## This is not working great so far
            array = hf.get(self.vid)[:,:,:,zl:zu,:]
        return array