from rest_framework.generics import ListAPIView, RetrieveAPIView

from ..utils.exceptions import ResourceNotFoundException
from ..views import UnauthenticatedAPIView
from .models import Question
from .serializers import QuestionSerializer


class QuestionRetrieveAPIView(UnauthenticatedAPIView, RetrieveAPIView):
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


class QuestionListAPIView(UnauthenticatedAPIView, ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return self.queryset.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["include_votes"] = (
            self.request.GET.get("include_votes", "").casefold() == "true"
        )
        return context


question_retrieve_api_view = QuestionRetrieveAPIView.as_view()
question_list_api_view = QuestionListAPIView.as_view()
