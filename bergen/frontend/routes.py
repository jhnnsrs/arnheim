
from rest_framework import routers

from frontend.views import FrontEndNodeViewSet

router = routers.SimpleRouter()
router.register(r"frontends", FrontEndNodeViewSet)