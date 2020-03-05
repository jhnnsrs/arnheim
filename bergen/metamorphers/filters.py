
from django_filters import rest_framework as filters

from metamorphers.models import Display


class DisplayFilter(filters.FilterSet):
    sample = filters.NumberFilter(field_name="representation__sample")

    class Meta:
        model = Display
        fields = ("creator","representation","representation__sample","sample")