from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from answers.managers import AnswerManager
from elements.models import Sample, Experiment, Pandas


class Question(models.Model):
    name = models.CharField(max_length=500)
    querystring = models.TextField(blank=True, null=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Question asked at {0}".format(self.created_at.strftime("%m/%d/%Y, %H:%M:%S"))


class Oracle(models.Model):
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, null=True, blank=True)
    defaultsettings = models.CharField(max_length=400)  # json decoded standardsettings

    def __str__(self):
        return "{0} at Channel {1}".format(self.name, self.channel)


class Answering(models.Model):
    oracle = models.ForeignKey(Oracle, on_delete=models.CASCADE)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    override = models.BooleanField()
    settings = models.CharField(max_length=1000)  # jsondecoded
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    error = models.CharField(max_length=300, blank=True, null=True)

    statuscode = models.IntegerField(blank=True, null=True)
    statusmessage = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return "Answering for Oracle {1} created at {0}".format(self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),self.oracle.name)


class Answer(models.Model):
    signature = models.CharField(max_length=300, null=True, blank=True)
    nodeid = models.CharField(max_length=400, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    vid = models.CharField(max_length=4000)
    shape = models.CharField(max_length=400, blank=True, null=True)
    name = models.CharField(max_length=4000, blank=True, null=True)
    key = models.CharField(max_length=4000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    pandas = models.ForeignKey(Pandas, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    objects = AnswerManager()

    def __str__(self):
        return self.name

    def to_pandas(self):
        return self.pandas.get_dataframe()
