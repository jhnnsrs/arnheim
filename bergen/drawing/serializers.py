from rest_framework import serializers

from drawing.models import LineROI


class LineROISerializer(serializers.ModelSerializer):
    transformations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = LineROI
        fields = "__all__"


