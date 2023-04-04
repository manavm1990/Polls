from rest_framework.response import Response

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
        serializer = QuestionSerializer(
            self.get_object(), context={"include_votes": include_results}
        )
        return Response(serializer.data)


question_retrieve_api_view = QuestionRetrieveAPIView.as_view()
