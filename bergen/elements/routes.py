
from rest_framework import routers

from elements.views import AntibodyViewSet

router = routers.SimpleRouter()
router.register(r"antibodies", AntibodyViewSet)