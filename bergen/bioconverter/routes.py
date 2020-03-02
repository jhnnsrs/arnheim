
from rest_framework import routers

from bioconverter.views import *

router = routers.SimpleRouter()
router.register(r"converters", ConverterViewSet)
router.register(r"conversings", ConversingViewSet)
router.register(r"bioimages", BioImageViewSet)
router.register(r"lockers", LockerViewSet)
router.register("bioseries", BioSeriesViewSet)
router.register("analyzings", AnalyzingViewSet)
router.register("analyzers", AnalyzerViewSet)