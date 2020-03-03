from graphene_django_extras import DjangoObjectType

from bioconverter.models import BioSeries, BioImage
from drawing.models import LineROI

class BioImageType(DjangoObjectType):
    class Meta:
        model = BioImage
        description = "All BioImages"
        filter_fields = {
            "creator": ("exact",),
            "name": ("icontains", "iexact"),
        }

class BioSeriesType(DjangoObjectType):
    class Meta:
        model = BioSeries
        description = "All BioSeries"
        filter_fields = {
            "creator": ("exact",),
            "bioimage__name": ("icontains", "iexact"),
        }


