
from rest_framework import routers

from flow.views import *

router = routers.SimpleRouter()
router.register(r"flows", FlowViewSet)
# DEPRECETAD
router.register(r"filterflows", FlowViewSet)
router.register(r"nodes", NodeViewSet)
router.register(r"layouts", LayoutViewSet)
router.register(r"foreignnode", ForeignNodeRequestViewSet)
router.register(r"foreignnodestatus", ForeignNodeStatusViewSet)
router.register(r"externals", ExternalViewSet)
router.register(r"externalrequests", ExternalRequestViewSet)