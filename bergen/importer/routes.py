
from rest_framework import routers

from importer.views import *

router = routers.SimpleRouter()
router.register(r"importers", ImporterViewSet)
router.register(r"importings", ImportingViewSet)