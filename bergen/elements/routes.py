
from rest_framework import routers

from elements.views import AntibodyViewSet, SampleViewSet, ExperimentViewSet

router = routers.SimpleRouter()
router.register(r"antibodies", AntibodyViewSet)
router.register(r"samples", SampleViewSet)
router.register(r"experiments", ExperimentViewSet)