
from rest_framework import routers

from flow.views import *

router = routers.SimpleRouter()
router.register(r"flows", FlowViewSet)
router.register(r"filterflows", FilterFlowViewSet)
router.register(r"conversionflows", ConversionFlowViewSet)