
from rest_framework import routers

from answers.views import *

router = routers.SimpleRouter()
router.register(r"answers", AnswerViewSet)
router.register(r"answerings", AnsweringViewSet)
router.register(r"questions", QuestionViewSet)
router.register(r"oracles", OracleViewSet)