from rest_framework import serializers

from evaluators.models import Data, Evaluating, Evaluator, VolumeData, ClusterData, LengthData


class EvaluatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluator
        fields = "__all__"


class EvaluatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluating
        fields = "__all__"

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = "__all__"

class VolumeDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = VolumeData
        fields = "__all__"

class ClusterDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClusterData
        fields = "__all__"

class LengthDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = LengthData
        fields = "__all__"