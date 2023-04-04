from django.apps import AppConfig


class QuestionsConfig(AppConfig):
    """
    QuestionsConfig is a configuration class for the "questions" app
    inside the "polls" project. It sets the default_auto_field and the
    app name.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "polls.questions"
