from django.contrib.auth.models import User
from rest_framework import serializers

from drawing.models import ROI, Sample, Experiment, BioMeta
from social.serializers import UserSerializer
from trontheim.viewsets import PublishingViewSet


class RoiSerializer(serializers.ModelSerializer):
    transformations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = ROI
        fields = "__all__"

class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = "__all__"

class BioMetaSerializer(serializers.ModelSerializer):
    sample = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = BioMeta
        exclude = ('json',)

class SampleSerializer(serializers.ModelSerializer):
    representations =  serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Sample
        fields = ("id","location","representations","experiment","creator","name","nodeid","bioseries")


