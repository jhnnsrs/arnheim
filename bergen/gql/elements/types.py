from graphene_django_extras import DjangoObjectType

from elements.models import Experiment, Sample, ExperimentalGroup, ROI


class ExperimentType(DjangoObjectType):
    class Meta:
        model = Experiment
        description = "All the Experiments  "
        filter_fields = {
            "creator": ("exact",),
            "description": ("icontains", "iexact"),
            "name": ("icontains", "iexact"),
        }
        exclude_fields = ['tags']


class SampleType(DjangoObjectType):
    class Meta:
        model = Sample
        description = " All the Samples stored in Oslo "
        filter_fields = {
            "creator": ("exact",),
            "experiment__name": ("icontains", "iexact"),
            "bioseries__name": ("icontains", "iexact"),
        }


class ExperimentalGroupType(DjangoObjectType):
    class Meta:
        model = ExperimentalGroup
        description = " All the ExperimentalGroups stored in Oslo "
        filter_fields = {
            "creator": ("exact",),
        }


class RoiType(DjangoObjectType):
    class Meta:
        model = ROI
        description = "All the Rois"
        filter_fields = {
            "creator": ("exact",),
            "representation__name": ("icontains", "iexact"),
        }


