
from rest_framework import routers

from nodes.views import *

router = routers.SimpleRouter()
router.register(r"nodes", NodeViewSet)
router.register(r"nodevariety", NodeVarietyViewSet)
router.register(r"arnheimhost", ArnheimHostViewSet)
router.register(r"nodeelement", NodeElementViewSet)