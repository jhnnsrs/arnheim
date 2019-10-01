from rest_framework import serializers

from visualizers.models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ExcelExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelExport
        fields = "__all__"

class VisualizingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visualizing
        fields = "__all__"


class VisualizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visualizer
        fields = "__all__"



