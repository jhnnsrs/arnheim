
from rest_framework import routers

from social.views import UserViewSet, CommentsViewSet, MeViewSet

router = routers.SimpleRouter()
router.register(r"me", MeViewSet)