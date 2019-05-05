from rest_framework import serializers

from elements.models import Antibody


class AntibodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Antibody
        fields = "__all__"