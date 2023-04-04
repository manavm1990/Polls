from rest_framework import viewsets

from ...views import UnauthenticatedAPIView
from ..models import Question
from .serializers import QuestionSerializer


class QuestionViewSet(UnauthenticatedAPIView, viewsets.ReadOnlyModelViewSet):
    """
    QuestionViewSet is a read-only viewset for the Question model.

    Inherits from UnauthenticatedAPIView to disable authentication and
    permission checks.

    Provides list and retrieve actions for Questions, including related
    Choices serialized using the QuestionSerializer. The number of votes
    for each choice can be included in the response using the
    "include_votes" query parameter.
    """

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_url_kwarg = "question_id"

    def get_object(self) -> Question:
        self.kwargs.get(self.lookup_url_kwarg)
        return super().get_object()

    def get_serializer_context(self) -> dict:
        context = super().get_serializer_context()
        context["include_votes"] = (
            self.request.GET.get("include_votes", "").casefold() == "true"
        )
        return context
