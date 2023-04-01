from rest_framework.response import Response

from ..utils.exceptions import ResourceNotFoundException

# '..' is akin to '../' in a file system
from ..views import UnauthenticatedAPIView
from .models import Question
from .serializers import QuestionSerializer


class QuestionAPIView(UnauthenticatedAPIView):
    @staticmethod
    def get(request, question_id, *args, **kwargs):
        """Show a single question and its choices. Optionally include the number of votes for each choice."""
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise ResourceNotFoundException(
                model_name="Question", requested_id=question_id
            )

        include_results = request.GET.get("include_votes", "").casefold() == "true"
        return Response(
            QuestionSerializer(
                question, context={"include_votes": include_results}
            ).data
        )


question_api_view = QuestionAPIView.as_view()
