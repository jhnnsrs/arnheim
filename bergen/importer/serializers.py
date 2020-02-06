from rest_framework import serializers

from importer.models import *


class ImporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Importer
        fields = "__all__"

class ImportingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Importing
        fields = "__all__"


