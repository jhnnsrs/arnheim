
from rest_framework import routers

from bioconverter.views import *

router = routers.SimpleRouter()
router.register(r"converters", ConverterViewSet)
router.register(r"conversings", ConversingViewSet)