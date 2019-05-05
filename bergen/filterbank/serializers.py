from django.contrib.auth.models import User
from rest_framework import serializers

from filterbank.models import Parsing, Filter, Representation, Filtering


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = "__all__"


class ParsingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parsing
        fields = "__all__"

class FilteringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filtering
        fields = "__all__"

class RepresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representation
        fields = "__all__"


