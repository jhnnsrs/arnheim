from rest_framework import serializers

from flow.models import *


class FlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = "__all__"


class FilterFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterFlow
        fields = "__all__"


class ConversionFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionFlow
        fields = "__all__"