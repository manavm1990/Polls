from rest_framework import viewsets

from ...utils.exception_handlers import ResourceNotFoundException
from ...views import UnauthenticatedAPIView
from ..models import Question
from .serializers import QuestionSerializer


class QuestionViewSet(UnauthenticatedAPIView, viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_url_kwarg = "question_id"

    def get_object(self):
        question_id = self.kwargs.get(self.lookup_url_kwarg)
        try:
            return super().get_object()
        except Question.DoesNotExist:
            raise ResourceNotFoundException(
                model_name="Question", requested_id=question_id
            )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["include_votes"] = (
            self.request.GET.get("include_votes", "").casefold() == "true"
        )
        return context
