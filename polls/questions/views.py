from ..utils.exceptions import ResourceNotFoundException
from ..views import UnauthenticatedRetrieveAPIView
from .models import Question
from .serializers import QuestionSerializer


class QuestionAPIView(UnauthenticatedRetrieveAPIView):
    """
    Show a single question and its choices. Optionally includes the number of votes for each choice.
    """

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_url_kwarg = "question_id"

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Question.DoesNotExist:
            raise ResourceNotFoundException(
                model_name="Question", requested_id=kwargs.get("question_id", "unknown")
            )


question_api_view = QuestionAPIView.as_view()
