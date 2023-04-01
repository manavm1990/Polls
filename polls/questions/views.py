from rest_framework.response import Response

from ..utils.exceptions import ResourceNotFoundException

# '..' is akin to '../' in a file system
from ..views import UnauthenticatedAPIView
from .models import Question


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

        include_results = request.GET.get("include_results", "").casefold() == "true"

        response_data = {
            "id": question.id,
            "text": question.question_text,
            "pub_date": question.pub_date,
            "choices": [
                {
                    "id": choice.id,
                    "text": choice.choice_text,
                    **({"votes": choice.votes} if include_results else {}),
                }
                for choice in question.choice_set.all()
            ],
        }

        # Use `Response` instead of `JsonResponse` for numerous DRF benefits even if just working with JSON
        return Response(response_data)


question_api_view = QuestionAPIView.as_view()
