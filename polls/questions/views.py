from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

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

    def get(self, request, *args, **kwargs):
        include_votes = request.GET.get("include_votes", "").casefold() == "true"
        serializer = QuestionSerializer(
            self.get_object(), context={"include_votes": include_votes}
        )
        return Response(serializer.data)


class QuestionListAPIView(UnauthenticatedAPIView, ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    # Ensure that a fresh queryset is used for each request (no caching stuff).
    def get_queryset(self):
        # Create a new queryset based on the original for the class ☝️.
        return self.queryset.all()

    def get(self, request, *args, **kwargs):
        include_votes = request.GET.get("include_votes", "").casefold() == "true"
        serializer = QuestionSerializer(
            self.get_queryset(), many=True, context={"include_votes": include_votes}
        )
        return Response(serializer.data)


question_retrieve_api_view = QuestionRetrieveAPIView.as_view()
question_list_api_view = QuestionListAPIView.as_view()
