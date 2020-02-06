from rest_framework import serializers

from filters.models import Filter, Filtering


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = "__all__"


class FilteringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filtering
        fields = "__all__"


