
from rest_framework import routers

from transformers.views import TransformerViewSet, TransformingViewSet
from elements.views import TransformationViewSet

router = routers.SimpleRouter()
router.register(r"transformers", TransformerViewSet)
router.register(r"transformings", TransformingViewSet)
router.register(r"transformations", TransformationViewSet)