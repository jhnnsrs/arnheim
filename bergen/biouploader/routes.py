
from rest_framework import routers

from biouploader.views import BioImageViewSet, BioSeriesViewSet, AnalyzingViewSet, AnalyzerViewSet, LockerViewSet

router = routers.SimpleRouter()
router.register(r"bioimages", BioImageViewSet)
router.register(r"lockers", LockerViewSet)
router.register("bioseries", BioSeriesViewSet)
router.register("analyzings", AnalyzingViewSet)
router.register("analyzers", AnalyzerViewSet)