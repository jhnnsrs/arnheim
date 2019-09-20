from rest_framework import serializers

from metamorphers.models import Metamorpher, Metamorphing, Display, Exhibit


class DisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Display
        fields = "__all__"


class ExhibitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exhibit
        fields = "__all__"


class MetamorpherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metamorpher
        fields = "__all__"


class MetamorphingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metamorphing
        fields = "__all__"
