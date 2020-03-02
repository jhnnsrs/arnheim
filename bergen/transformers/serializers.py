from rest_framework import serializers

from transformers.models import Transformer, Transforming
from elements.models import Transformation


class TransformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transformer
        fields = "__all__"


class TransformingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transforming
        fields = "__all__"

class TransformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transformation
        fields = "__all__"


