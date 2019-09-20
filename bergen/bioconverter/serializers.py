from rest_framework import serializers

from bioconverter.models import Converter, Conversing, Representation


class ConverterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Converter
        fields = "__all__"


class ConversingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversing
        fields = "__all__"


class RepresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representation
        fields = "__all__"