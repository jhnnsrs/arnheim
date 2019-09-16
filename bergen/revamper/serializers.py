from rest_framework import serializers

from revamper.models import *


class RevamperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revamper
        fields = "__all__"

class RevampingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revamping
        fields = "__all__"

class MaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mask
        fields = "__all__"
