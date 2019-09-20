from rest_framework import serializers

from elements.models import Antibody, Experiment, Sample


class AntibodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Antibody
        fields = "__all__"


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = "__all__"


class SampleSerializer(serializers.ModelSerializer):
    representations =  serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Sample
        fields = ("id","location","representations","experiment","creator","name","nodeid","bioseries")