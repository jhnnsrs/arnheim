from rest_framework import serializers

from drawing.models import ROI


class RoiSerializer(serializers.ModelSerializer):
    transformations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = ROI
        fields = "__all__"


