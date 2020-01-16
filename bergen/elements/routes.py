
from rest_framework import routers

from elements.views import AntibodyViewSet, SampleViewSet, ExperimentViewSet, ExperimentalGroupViewSet, AnimalViewSet, \
    FileMatchStringViewSet, NumpyViewSet, ZarrViewSet

router = routers.SimpleRouter()
router.register(r"antibodies", AntibodyViewSet)
router.register(r"samples", SampleViewSet)
router.register(r"experiments", ExperimentViewSet)
router.register(r"experimentalgroups", ExperimentalGroupViewSet)
router.register(r"animals", AnimalViewSet)
router.register(r"filematchstrings", FileMatchStringViewSet)
router.register(r"numpys", NumpyViewSet)
router.register(r"zarrs", ZarrViewSet)