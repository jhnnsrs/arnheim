from rest_framework import serializers

from mutaters.models import *
from nodes.models import *


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = "__all__"


class NodeVarietySerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeVariety
        fields = "__all__"

class ArnheimHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArnheimHost
        fields = "__all__"

class NodeElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeElement
        fields = "__all__"


