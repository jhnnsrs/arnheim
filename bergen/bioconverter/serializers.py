from django.contrib.auth.models import User
from rest_framework import serializers

from bioconverter.models import ConversionRequest, Converter, ConvertToSampleRequest, JobRequest, Conversing
from filterbank.models import Parsing, Filter, Representation


class ConverterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Converter
        fields = "__all__"


class ConversionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionRequest
        fields = "__all__"

class ConversingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversing
        fields = "__all__"

class ConvertToSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvertToSampleRequest
        fields = "__all__"

class JobRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRequest
        fields = "__all__"




