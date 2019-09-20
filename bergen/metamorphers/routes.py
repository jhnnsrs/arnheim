
from rest_framework import routers

from metamorphers.views import *

router = routers.SimpleRouter()
router.register(r"metamorphers", MetamorpherViewSet)
router.register(r"metamorphings", MetamorphingViewSet)
router.register(r"displays", DisplayViewSet)
router.register(r"exhibits", ExhibitViewSet)