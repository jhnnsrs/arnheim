from rest_framework import serializers

from biouploader.models import BioImage, BioSeries, Analyzing, Analyzer, Locker


class BioImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BioImage
        fields = "__all__"



class BioSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BioSeries
        fields = "__all__"

class LockerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locker
        fields = "__all__"

class AnalyzingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analyzing
        fields = "__all__"

class AnalyzerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analyzer
        fields = "__all__"