from rest_framework import serializers

from metamorphers.models import Metamorpher, Metamorphing, Display, Exhibit, Kafkaing


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

class KafkaingSerializer(serializers.ModelSerializer):
    MESSAGE_TYPE = 'kafkaing'
    VERSION = 1
    KEY_FIELD = 'id'

    class Meta:
        model = Kafkaing
        fields = "__all__"


class KafkaingMessageSerializer(serializers.ModelSerializer):
    MESSAGE_TYPE = 'kafkaing2'
    VERSION = 1
    KEY_FIELD = 'id'

    class Meta:
        model = Kafkaing
        fields = "__all__"
        depth = 2