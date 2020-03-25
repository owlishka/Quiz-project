from rest_framework import serializers
from quiz.models import Question, QuestionStat


class QuestionSerializer(serializers.ModelSerializer):
    test = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Question
        exclude = ("is_active",)


class QuestionListSerializer(QuestionSerializer):
    update_url = serializers.URLField(source="get_update_url")
    option1 = serializers.CharField(source="wrong_answer_1", read_only=True)
    option2 = serializers.CharField(source="wrong_answer_2", read_only=True)
    option3 = serializers.CharField(source="wrong_answer_3", read_only=True)
    option4 = serializers.CharField(source="correct_answer", read_only=True)

    class Meta:
        model = Question
        fields = ("question", "update_url", "option1", "option2", "option3", "option4")


class QuestionStatSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(read_only=True)
    correct_answer = serializers.CharField(default=None)

    class Meta:
        model = QuestionStat
        exclude = ("candidate", "is_correct")

