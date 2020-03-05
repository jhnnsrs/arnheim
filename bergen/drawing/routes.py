
from rest_framework import routers

from drawing.views import LineROIViewSet

router = routers.SimpleRouter()
router.register(r"linerois", LineROIViewSet)