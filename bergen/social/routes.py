
from rest_framework import routers

from social.views import UserViewSet, CommentsViewSet, MeViewSet

router = routers.SimpleRouter()
router.register(r"users", UserViewSet)
router.register(r"comments", CommentsViewSet)
router.register(r"me", MeViewSet)