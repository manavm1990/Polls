from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)  # CharField requires a max_length
    pub_date = models.DateTimeField(
        "date published"
    )  # Optional argument for human-readable name


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
