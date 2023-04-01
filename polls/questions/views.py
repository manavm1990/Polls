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
        # "Unexpected type(s):(str, bool)Possible type(s):(MultiValueDict[str, str], str)(MultiValueDict[str, str],
        # str)"
        # BS false positive from PyCharm 'Professional' edition. 🙄 https://youtrack.jetbrains.com/issue/PY-37457

        # noinspection PyTypeChecker
        include_results = (
            self.request.GET.get("include_results", "").casefold() == "true"
        )

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
                        # '**' is the spread operator in Python. It's like the '...' in JavaScript (with same caveats).
                        **({"votes": choice.votes} if include_results else {}),
                    }
                    for choice in question.choice_set.all()
                ],
            }
        )


question_detail_view = QuestionDetailView.as_view()
