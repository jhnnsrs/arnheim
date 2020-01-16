from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from answers.models import Answer
from visualizers.managers import ProfileManager, ExcelExportManager


class Visualizer(models.Model):
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, null=True, blank=True)
    defaultsettings = models.CharField(max_length=400)  # json decoded standardsettings

    def __str__(self):
        return "{0} at Channel {1}".format(self.name, self.channel)


class Visualizing(models.Model):
    visualizer = models.ForeignKey(Visualizer, on_delete=models.CASCADE)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    override = models.BooleanField()
    status = models.CharField(max_length=40, default="STARTED")
    settings = models.CharField(max_length=1000)  # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    error = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return "Visualizing for Visualizer {1} created at {0}".format(self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),self.visualizer.name)


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
