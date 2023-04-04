import pytest

from .models import Question


@pytest.mark.django_db
@pytest.fixture
def question(db):
    question = Question.objects.create(question_text="What's up?")
    question.choices.create(choice_text="Not much", votes=0)
    question.choices.create(choice_text="The sky", votes=0)
    return question


def test_pub_date_is_read_only(question):
    question.pub_date = "2020-01-01"
    question.save()
    assert question.pub_date != "2020-01-01"
