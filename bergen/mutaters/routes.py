
from rest_framework import routers

from mutaters.views import *

router = routers.SimpleRouter()
router.register(r"mutaters", MutaterViewSet)
router.register(r"mutatings", MutatingViewSet)
router.register(r"reflections", ReflectionViewSet)
router.register(r"reflectionss", ReflectionViewSet)