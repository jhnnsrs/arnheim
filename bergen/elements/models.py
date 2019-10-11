import os

import h5py
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from pandas import HDFStore
from taggit.managers import TaggableManager

from biouploader.models import BioSeries, BioMeta
from elements.managers import NumpyManager, PandasManager
from elements.utils import toFileName
from mandal import settings


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Antibody(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}".format(self.name)


class Experiment(models.Model):
    name = models.CharField(max_length=200)
    tags = TaggableManager()
    description = models.CharField(max_length=1000)
    description_long = models.TextField(null=True,blank=True)
    linked_paper = models.URLField(null=True,blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='experiment_banner',null=True,blank=True)

    def __str__(self):
        return "Experiment {0} by {1}".format(self.name,self.creator.username)

class ExperimentalGroup(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    iscontrol = models.BooleanField()


    def __str__(self):
        return "ExperimentalGroup {0} on Experiment {1}".format(self.name,self.experiment.name)

class FileMatchString(models.Model):
    name = models.CharField(max_length=500)
    regexp = models.CharField(max_length=4000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "FileMatchString {0} created by {1}".format(self.name,self.creator.name)


class Animal(models.Model):
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=400)
    type = models.CharField(max_length=500)
    creator = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, blank=True, on_delete=models.CASCADE, null=True)
    experimentalgroup = models.ForeignKey(ExperimentalGroup, blank=True, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{0}".format(self.name)


class Sample(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    location = models.CharField(max_length=400)
    name = models.CharField(max_length=1000)
    experiment = models.ForeignKey(Experiment, on_delete=models.SET_NULL, blank=True, null=True)
    bioseries = models.ForeignKey(BioSeries, on_delete=models.SET_NULL, blank=True, null=True)
    meta = models.ForeignKey(BioMeta, on_delete=models.CASCADE, blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    experimentalgroup = models.ForeignKey(ExperimentalGroup, on_delete=models.SET_NULL, blank=True, null=True)
    animal = models.ForeignKey(Animal, on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return "{0} by User: {1}".format(self.name,self.creator.username)


    def delete(self, *args, **kwargs):
        print("Trying to remove Sample H5File")
        for item in self.numpys.all():
            item.delete()

        filepath = os.path.join(settings.H5FILES_ROOT,toFileName(self))
        if os.path.isfile(filepath):
            os.remove(filepath)
            print("Removed Sample H5File",filepath)

        super(Sample, self).delete(*args, **kwargs)


class Numpy(models.Model):
    filepath = models.FilePathField(max_length=400) # aka h5files/$sampleid.h5
    vid = models.CharField(max_length=1000) # aca vid0, vid1, vid2, vid3
    type = models.CharField(max_length=100)
    dtype = models.CharField(max_length=300, blank=True, null=True)
    compression = models.CharField(max_length=300, blank=True, null=True)
    shape = models.CharField(max_length=400, blank=True, null=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name="numpys")
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

    def delete(self, *args, **kwargs):
        print("Trying to remove Dataset from Filepath", self.filepath)
        with h5py.File(self.filepath, 'a') as file:
            print("Trying to Access Vid from file {0} to delete array".format(self.filepath))
            hf = file[self.type]
            if self.vid in hf:
                del hf[self.vid]
                print("Delteted Vid {1} from file {0}".format(self.filepath,self.vid))

        super(Numpy, self).delete(*args, **kwargs)

    def __str__(self):
        return "Numpy Object with VID " + str(self.vid) + " at " + str(self.filepath)


class Pandas(models.Model):
    filepath = models.FilePathField(max_length=400) # aka pandas/$answerid.h5
    vid = models.CharField(max_length=1000) # aca vid0, vid1, vid2, vid3
    type = models.CharField(max_length=100)
    compression = models.CharField(max_length=300, blank=True, null=True)
    # Custom Manager to simply create an array
    objects = PandasManager()

    def get_dataframe(self):
        print("Trying to access file {0} to get dataframe".format(self.filepath))
        with HDFStore(self.filepath) as store:
            path = self.type + "/" + self.vid
            dataframe = store.get(path)
        return dataframe

    def set_dataframe(self,dataframe):
        print("Trying to access file {0} to set dataframe".format(self.filepath))
        with HDFStore(self.filepath) as store:
            path = self.type + "/" + self.vid
            store.put(path, dataframe)

    def delete(self, *args, **kwargs):
        print("Trying to remove Dataframe from Filepath", self.filepath)
        with HDFStore(self.filepath) as store:
            path = self.type + "/" + self.vid
            if path in store:
                store.delete(path)
                print("Deleted Dataframe with VID {1} from file {0}".format(self.filepath, self.vid))

        super(Pandas, self).delete(*args, **kwargs)

    def __str__(self):
        return "Pandas with VID " + str(self.vid) + " at " + str(self.filepath)