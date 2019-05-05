from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Antibody(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}".format(self.name)