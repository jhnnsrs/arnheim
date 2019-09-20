
from rest_framework import routers

from evaluators.views import EvaluatorViewSet, EvaluatingViewSet, DataViewSet, VolumeDataViewSet, ClusterDataViewSet

router = routers.SimpleRouter()
router.register(r"evaluators", EvaluatorViewSet)
router.register(r"evaluatings", EvaluatingViewSet)
router.register(r"data", DataViewSet)
router.register(r"volumedata", VolumeDataViewSet)
router.register(r"clusterdata", ClusterDataViewSet)