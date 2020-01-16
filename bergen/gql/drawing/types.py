from graphene_django_extras import DjangoObjectType

from drawing.models import ROI


class RoiType(DjangoObjectType):
    class Meta:
        model = ROI
        description = "All the Rois"
        filter_fields = {
            "creator": ("exact",),
            "display__name": ("icontains", "iexact"),
        }


