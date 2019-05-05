import os

import h5py
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models

# Create your models here.
from drawing.models import Sample
from filterbank.modelmanagers import NpArrayManager
from multichat import settings
from representations.models import Experiment


class NpArray(models.Model):
    file = models.FilePathField() # aka h5files/$sampleid.h5
    position = models.CharField(max_length=100) # aca vid0, vid1, vid2, vid3

    # Custom Manager to simply create an array
    objects = NpArrayManager()

    def get_array(self):
        with h5py.File(self.file, 'a') as file:
            print("Trying to access file {0} to get array".format(self.file))
            hf = file["representations"]
            array = hf.get(self.position).value
        return array

    def set_array(self,array):
        with h5py.File(self.file, 'a') as file:
            print("Trying to access file {0} to set array".format(self.file))
            hf = file["representations"]
            if self.position in hf: del hf[self.position]
            hf.create_dataset(self.position, data=array)

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name):
        """Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class AImage(models.Model):
    image = models.ImageField(upload_to="representation_images", blank=True, null=True)


class RepresentationManager(models.Manager):
    def create(self, **obj_data):
        # Do some extra stuff here on the submitted data before saving...
        # For example...
        if "numpy" in obj_data:
            print("Creating Representation with help of np.array")
            sample: Sample = obj_data["sample"]
            filepath = sample.name + ".h5"
            position = "vid_{0}".format(str(obj_data["nodeid"]))

            # TODO: if sample is not provided this should raise an exception
            numpy = NpArray.objects.create(filepath=filepath, nparray=obj_data["numpy"], position=position)


            obj_data["nparray"] = numpy
            del obj_data["numpy"]

        # Now call the super method which does the actual creation
        return super().create(**obj_data)  # Python 3 syntax!!

class Dicom(models.Model):
    file = models.FileField(upload_to="representation_dicoms")

class Nifti(models.Model):
    file = models.FilePathField()

class Representation(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    vid = models.IntegerField(blank=True, null=True)
    inputrep = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null= True)
    shape = models.CharField(max_length=100, blank=True, null= True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE,related_name='representations')
    nparray = models.ForeignKey(NpArray, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ForeignKey(AImage, on_delete=models.CASCADE,  blank=True, null=True)
    dicom = models.ForeignKey(Dicom, on_delete=models.CASCADE, blank=True, null=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    meta = models.CharField(max_length=6000, null=True, blank=True)

    objects = RepresentationManager()

    def __str__(self):
        return self.name



class Filter(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=500)
    channel = models.CharField(max_length=100, null=True, blank=True)
    inputmodel = models.CharField(max_length=1000, null=True, blank=True)
    outputmodel = models.CharField(max_length=1000, null=True, blank=True)

    defaultsettings = models.CharField(max_length=400) #json decoded standardsettings

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.path)


class Filtering(models.Model):
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE)
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    settings = models.CharField(max_length=1000) # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE,blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)


class Parsing(models.Model):
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE)
    returnchannel = models.CharField(max_length=100)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    settings = models.CharField(max_length=1000) # jsondecoded
    progress = models.IntegerField(blank=True,null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE,blank=True, null=True)
    # The inputvid will pe parsed to the output vid (if no representation in that slot exists it will be created
    # otherwise just updated
    inputvid = models.IntegerField()
    outputvid = models.IntegerField()

    def __str__(self):
        return "Parsing Request for Filter: {0}".format(self.filter)

