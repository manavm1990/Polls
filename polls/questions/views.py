from rest_framework.response import Response

from ..utils.exceptions import ResourceNotFoundException
from ..views import UnauthenticatedRetrieveAPIView
from .models import Question
from .serializers import QuestionSerializer


class QuestionRetrieveAPIView(UnauthenticatedRetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_url_kwarg = "question_id"

    def get(self, request, *args, **kwargs):
        """Show a single question and its choices. Optionally include the number of votes for each choice."""
        include_results = request.GET.get("include_votes", "").casefold() == "true"
        try:
            super().get(request, *args, **kwargs)
        except Question.DoesNotExist:
            raise ResourceNotFoundException(
                model_name="Question", requested_id=kwargs["question_id"]
            )

        serializer = QuestionSerializer(
            self.get_object(), context={"include_votes": include_results}
        )
        return Response(serializer.data)


question_retrieve_api_view = QuestionRetrieveAPIView.as_view()
