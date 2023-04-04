from rest_framework.serializers import ModelSerializer

from polls.questions.models import Choice, Question


class ChoiceSerializer(ModelSerializer):
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
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "question_text",
            "pub_date",
            "choices",
        ]  # 'choices' is the 'related_name' from the Choice model
