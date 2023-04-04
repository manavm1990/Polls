import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    The Question model represents a question in the polling app.
    It has a text and a publication date.
    """

    question_text = models.CharField(max_length=200)  # CharField requires a max_length
    pub_date = models.DateTimeField(
        "date published", auto_now_add=True
    )  # This uses an optional argument for human-readable name

    def __str__(self) -> str:
        return self.question_text

    @property
    def text(self) -> str:
        return self.question_text

    @property
    def was_published_recently(self) -> bool:
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Question"
        verbose_name_plural = "Questions"


class Choice(models.Model):
    """
    The Choice model represents a possible answer to a question.
    It is associated with a question and has a text and a vote count.
    """

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text
