from django.http import JsonResponse
# The DetailView automatically 🪄 handles the logic for fetching from the database based on the primary key in the URL.
from django.views.generic import DetailView

from .models import Question


class QuestionDetailView(DetailView):
    model: type[Question] = Question

    # This is the column in the database for the lookup.
    slug_field = "id"

    # This is the name of the URL parameter that contains the lookup value.
    slug_url_kwarg = "question_id"

    # TODO: Handle the case where the question doesn't exist.
    def render_to_response(self, context, **response_kwargs) -> JsonResponse:
        """Return a JSON response with the question and its choices."""
        question = self.object

        return JsonResponse(
            {
                "id": question.id,
                "text": question.question_text,
                "pub_date": question.pub_date,
                "choices": [
                    {
                        "id": choice.id,
                        "text": choice.choice_text,
                        "votes": choice.votes,
                    }
                    for choice in question.choice_set.all()
                ],
            }
        )


question_detail_view = QuestionDetailView.as_view()
