
from rest_framework import routers

from biouploader.views import BioMetaViewSet
from drawing.views import RoiViewSet, RepresentationViewSet
from elements.views import SampleViewSet, ExperimentViewSet

router = routers.SimpleRouter()
router.register(r"rois", RoiViewSet)
router.register(r"samples", SampleViewSet)
router.register(r"samplelist", SampleViewSet)
router.register(r"experiments", ExperimentViewSet)
router.register(r"representations", RepresentationViewSet)
router.register(r"biometas", BioMetaViewSet)