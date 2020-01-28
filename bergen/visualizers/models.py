from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from answers.models import Answer
from larvik.models import LarvikJob, LarvikConsumer
from visualizers.managers import ProfileManager, ExcelExportManager


class Visualizer(LarvikConsumer):
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, null=True, blank=True)
    defaultsettings = models.CharField(max_length=400)  # json decoded standardsettings

    def __str__(self):
        return "{0} at Channel {1}".format(self.name, self.channel)


class Visualizing(LarvikJob):
    visualizer = models.ForeignKey(Visualizer, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return "Visualizing for Visualizer {0}".format(self.visualizer.name)


class Profile(models.Model):
    signature = models.CharField(max_length=300, null=True, blank=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    vid = models.CharField(max_length=4000)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=4000, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    htmlfile = models.FileField(upload_to="profiles",blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    def __str__(self):
        return self.name



class ExcelExport(models.Model):
    signature = models.CharField(max_length=300, null=True, blank=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    vid = models.CharField(max_length=4000)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=4000, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    excelfile = models.FileField(upload_to="excels",blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    objects = ExcelExportManager()

    def __str__(self):
        return self.name
