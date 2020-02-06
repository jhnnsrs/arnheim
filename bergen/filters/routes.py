
from rest_framework import routers

from filters.views import FilteringViewSet, FilterViewSet

router = routers.SimpleRouter()
router.register(r"filters", FilterViewSet)
router.register(r"filterings", FilteringViewSet)