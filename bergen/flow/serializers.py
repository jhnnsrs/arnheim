from rest_framework import serializers

from flow.models import Flow, Node, Layout, ForeignNodeRequest, ForeignNodeStatus


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


class ForeignNodeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignNodeRequest
        fields = "__all__"

class ForeignNodeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignNodeStatus
        fields = "__all__"