
from rest_framework import routers

from visualizers.views import *

router = routers.SimpleRouter()
router.register(r"visualizers", VisualizerViewSet)
router.register(r"visualizings", VisualizingViewSet)
router.register(r"profiles", ProfileViewSet)
router.register(r"excelexports", ExcelExportViewSet)