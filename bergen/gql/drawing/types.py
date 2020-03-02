from graphene_django_extras import DjangoObjectType

from drawing.models import LineROI


class LineROIType(DjangoObjectType):
    class Meta:
        model = LineROI
        description = "All the Lines"
        filter_fields = {
            "creator": ("exact",),
            "representation__name": ("icontains", "iexact"),
        }


