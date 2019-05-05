from django.contrib.auth.models import User, Group
from django.db import models

# Create your models here.


class Flow(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True, blank=True)
    diagram = models.CharField(max_length=50000)
    description = models.CharField(max_length=50000)


class ConversionFlow(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True, blank=True)
    diagram = models.CharField(max_length=50000)
    description = models.CharField(max_length=50000)


class FilterFlow(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True, default="Not Set")
    diagram = models.CharField(max_length=50000)
    description = models.CharField(max_length=50000, default="Add a Description")