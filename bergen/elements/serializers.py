from rest_framework import serializers

from elements.models import Antibody, Experiment, Sample, ExperimentalGroup, Animal, FileMatchString, Representation, \
    ROI


class AntibodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Antibody
        fields = "__all__"

class AnimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Animal
        fields = "__all__"

class FileMatchStringSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileMatchString
        fields = "__all__"

class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = "__all__"

class ExperimentalGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentalGroup
        fields = "__all__"

class RepresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representation
        fields = "__all__"


class ROISerializer(serializers.ModelSerializer):
    class Meta:
        model = ROI
        fields = "__all__"



class SampleSerializer(serializers.ModelSerializer):
    representations =  serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    bioseries = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Sample
        fields = "__all__"


