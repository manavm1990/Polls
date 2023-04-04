from rest_framework.serializers import ModelSerializer

from polls.questions.models import Choice, Question


class ChoiceSerializer(ModelSerializer):
    """
    ChoiceSerializer handles serialization and deserialization for the
    Choice model.

    Provides serialization of Choice fields including the number of votes,
    which can be excluded using the context variable "include_votes".
    """

    class Meta:
        model = Choice
        fields = ["id", "choice_text", "votes"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        include_votes = self.context.get("include_votes", False)
        if not include_votes:
            rep.pop("votes")
        return rep


class QuestionSerializer(ModelSerializer):
    """
    QuestionSerializer handles serialization and deserialization for the
    Question model.

    Provides serialization of Question fields including related Choices,
    which are serialized using the ChoiceSerializer.
    """

    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "question_text",
            "pub_date",
            "choices",
        ]  # 'choices' is the 'related_name' from the Choice model
