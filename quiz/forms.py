from django.forms import ModelForm
from .models import Test, Question, Comment, QuestionStat


class AddQuizForm(ModelForm):
    class Meta:
        model = Question
        fields = [
            "question",
            "wrong_answer_1",
            "wrong_answer_2",
            "wrong_answer_3",
            "correct_answer",
        ]


class AddTestForm(ModelForm):

    class Meta:
        model = Test
        fields = ["name", "description"]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['message']


class AddAnswerForm(ModelForm):
    class Meta:
        model = QuestionStat
        fields = ['response']
