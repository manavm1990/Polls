import datetime
from contextlib import contextmanager

import pytest
from django.db import models
from django.db.models import DateTimeField
from django.utils import timezone

from .models import Question


@pytest.mark.django_db
@pytest.fixture
def question(db):
    question = Question.objects.create(question_text="What's up?")
    question.choices.create(choice_text="Not much", votes=0)
    question.choices.create(choice_text="The sky", votes=0)
    return question


@contextmanager
def remove_auto_now_add(model_field: type[models.DateTimeField]):
    """Context manager to temporarily remove auto_now_add from a model field for tests."""
    auto_now_add = model_field.auto_now_add
    model_field.auto_now_add = False
    yield
    model_field.auto_now_add = auto_now_add


@pytest.mark.django_db
@pytest.fixture
def old_question(db):
    # Supposedly we HAVE TO use 'noqa' here to satisfy PyCharm, etc.
    pub_date_field: type[DateTimeField] = Question._meta.get_field("pub_date")  # noqa
    with remove_auto_now_add(pub_date_field):
        old_question = Question.objects.create(
            question_text="What's up?",
            pub_date=timezone.now() - datetime.timedelta(days=2),
        )
    return old_question


def test_pub_date_is_read_only(question):
    question.pub_date = "2020-01-01"
    question.save()
    assert question.pub_date != "2020-01-01"


def test_was_published_recently(question):
    assert question.was_published_recently is True


def test_was_not_published_recently_with_old_question(old_question):
    assert old_question.was_published_recently is False
