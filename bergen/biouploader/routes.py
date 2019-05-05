
from rest_framework import routers

from biouploader.views import BioImageViewSet, BioSeriesViewSet, AnalyzingViewSet, AnalyzerViewSet, LockerViewSet
from drawing.views import RoiViewSet, SampleViewSet
from filterbank.views import FilterViewSet, ParsingRequestViewSet
from social.views import UserViewSet, CommentsViewSet

router = routers.SimpleRouter()
router.register(r"bioimages", BioImageViewSet)
router.register(r"lockers", LockerViewSet)
router.register("bioseries", BioSeriesViewSet)
router.register("analyzings", AnalyzingViewSet)
router.register("analyzers", AnalyzerViewSet)