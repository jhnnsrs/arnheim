from rest_framework import serializers

from mutaters.models import *


class MutaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mutater
        fields = "__all__"

class MutatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mutating
        fields = "__all__"

class ReflectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reflection
        fields = "__all__"
