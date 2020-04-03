import graphene
from graphene_django_extras import DjangoObjectType

from elements.filters import ExperimentFilter, SampleFilter
from elements.models import Experiment, Sample, ExperimentalGroup, ROI, Representation


class ExperimentType(DjangoObjectType):
    class Meta:
        model = Experiment
        description = "All the Experiments  "
        filterset_class = ExperimentFilter
        exclude_fields = ['tags']

    description = graphene.String(description="A short description of this Experiment")
    linked_paper = graphene.String(description="Pubmed link, if this experiment has already been published")


class SampleType(DjangoObjectType):
    class Meta:
        model = Sample
        description = " All the Samples stored in Oslo "
        filterset_class = SampleFilter




class RepresentationType(DjangoObjectType):
    class Meta:
        model = Representation
        description = " A representation is our model of a multidimensional representation of image data on a Sample. Each Sample can have multiple representations," \
                      " each constituting a differently filtered image stack. Representations share a common x and y axis and can share different z and time axes. 2D Rois" \
                      "therefore interchangable between different Representations"
        filter_fields = {
            "creator": ("exact",),
            "sample__name": ("icontains", "iexact"),
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


