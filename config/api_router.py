from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from polls.questions.api.views import QuestionViewSet
from polls.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("questions", QuestionViewSet)

app_name = "api"
urlpatterns = router.urls
