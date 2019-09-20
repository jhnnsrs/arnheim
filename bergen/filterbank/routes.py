
from rest_framework import routers

from filterbank.views import FilterViewSet, FilteringViewSet

router = routers.SimpleRouter()
router.register(r"filters", FilterViewSet)
router.register(r"filterings", FilteringViewSet)