from rest_framework import serializers

from strainers.models import Strainer, Straining


class StrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Strainer
        fields = "__all__"


class StrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Straining
        fields = "__all__"


