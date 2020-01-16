from rest_framework import serializers

from elements.models import Antibody, Experiment, Sample, ExperimentalGroup, Animal, FileMatchString, Numpy, Zarr


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

class NumpySerializer(serializers.ModelSerializer):
    class Meta:
        model = Numpy
        exclude = ("filepath",)


class SampleSerializer(serializers.ModelSerializer):
    representations =  serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Sample
        fields = "__all__"


class ZarrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zarr
        exclude =("store",)