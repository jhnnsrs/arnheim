from rest_framework import serializers

from flow.models import Flow, Node, Layout, External, ExternalRequest


class FlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = "__all__"


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = "__all__"


class LayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layout
        fields = "__all__"


class ExternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = External
        fields = "__all__"

class ExternalNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = External
        exclude = ("uniqueid",)


class ExternalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalRequest
        fields = "__all__"