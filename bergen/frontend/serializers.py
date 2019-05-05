from rest_framework import serializers

from frontend.models import FrontEndNode


class FrontEndNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrontEndNode
        fields = "__all__"