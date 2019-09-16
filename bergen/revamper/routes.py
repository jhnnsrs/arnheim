
from rest_framework import routers

from mutaters.views import *
from revamper.views import MaskViewSet, RevampingViewSet, RevamperViewSet

router = routers.SimpleRouter()
router.register(r"masks", MaskViewSet)
router.register(r"revampings", RevampingViewSet)
router.register(r"revamper", RevamperViewSet)