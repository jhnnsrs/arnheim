
from rest_framework import routers

from strainers.views import StrainerViewSet, StrainingViewSet

router = routers.SimpleRouter()
router.register(r"strainers", StrainerViewSet)
router.register(r"strainings", StrainingViewSet)