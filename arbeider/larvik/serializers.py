from rest_framework import serializers

from larvik.models import Zarr


class ZarrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zarr
        exclude =("store",)