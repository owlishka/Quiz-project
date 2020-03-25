from random import shuffle
import bleach
from django.http import Http404
from rest_framework import status
from rest_framework.generics import UpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.api.serializers import QuestionListSerializer, QuestionStatSerializer, QuestionSerializer
from quiz.models import Test, TestStat, Question, QuestionStat


class getQuestionList(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user_profile = self.request.user
        test = Test.objects.get(pk=self.kwargs.get('pk'))
        questions = Question.objects.filter(test=test)
        if not (
                user_profile == test.owner
                or TestStat.objects.filter(test=test, candidate=user_profile.id).exists()
        ):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionListSerializer(questions, many=True)
        for data in serializer.data:
            optionList = [
                data["option1"],
                data["option2"],
                data["option3"],
                data["option4"],
            ]
            shuffle(optionList)
            i = 0
            while i < 4:
                data["option" + str(i + 1)] = bleach.clean(optionList[i])
                i += 1
        return Response(serializer.data)


class QuestionStatForm(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        question = Question.objects.get(pk=self.kwargs.get('qpk'))
        teststat, create = TestStat.objects.get_or_create(test=question.test, candidate=self.request.user)
        questionstat, create = QuestionStat.objects.get_or_create(
            question=question, candidate=self.request.user
        )
        if teststat.has_completed:
            questionstat.correct_answer = question.correct_answer
        serializer = QuestionStatSerializer(questionstat)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs,):
        question = Question.objects.get(pk=self.kwargs.get('qpk'))
        teststat = TestStat.objects.get(test=question.test, candidate=self.request.user)
        questionstat, create = QuestionStat.objects.get_or_create(
            question=question, candidate=self.request.user
        )
        serializer = QuestionStatSerializer(questionstat, data=request.data)
        if serializer.is_valid():
            if teststat.has_completed:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user_response = request.POST.get("option", None)
            if user_response:
                questionstat.response = user_response
            questionstat.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScoreChart(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        test = Test.objects.get(pk=self.kwargs.get('pk'))
        teststat = TestStat.objects.get(test=test, candidate=self.request.user)
        if teststat.has_completed:
            correct_count = teststat.get_correct_response_count()
            wrong_count = teststat.get_wrong_response_count()
            total = teststat.get_total_attempts()
            colors = ["rgb(0,255,0)", "rgb(255,0,0)", "rgb(105,105,105)"]
            return Response(
                {
                    "correct_count": correct_count,
                    "wrong_count": wrong_count,
                    "total": total,
                    "colors": colors,
                }
            )


class UpdateQuestionForm(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        test = Test.objects.get(pk=self.kwargs.get('tpk'), owner=self.request.user)
        question = Question.objects.get(pk=self.kwargs.get('qpk'), test=test)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        test = Test.objects.get(pk=self.kwargs.get('tpk'), owner=self.request.user)
        question = Question.objects.get(pk=self.kwargs.get('qpk'), test=test)
        if test.is_active:
            raise Http404
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            questions = test.questions.all()
            serializer = QuestionListSerializer(questions, many=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        test = Test.objects.get(pk=self.kwargs.get('tpk'), owner=self.request.user)
        question = Question.objects.get(pk=self.kwargs.get('qpk'), test=test)
        if test.is_active:
            raise Http404
        question.delete()
        questions = test.questions.all()
        serializer = QuestionListSerializer(questions, many=True)
        return Response(serializer.data)


class ToggleTestActive(UpdateAPIView):
    permission_classes = [IsAuthenticated, ]

    def update(self, request, *args, **kwargs):
        test = Test.objects.get(pk=self.kwargs.get('pk'), owner=self.request.user)
        if not self.request.user.is_authenticated:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if test.questions.count() < 5:
            return Response(
                {"message": "Not enough questions! Please add at least 5"}, status=status.HTTP_400_BAD_REQUEST
            )
        test.is_active = not test.is_active
        test.save()
        return Response({"active": test.is_active}, status=status.HTTP_200_OK)


class AddQuestionForm(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs,):
        test = Test.objects.get(pk=self.kwargs.get('pk'), owner=self.request.user)
        if test.is_active:
            raise Http404
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(test=test)
            questions = Question.objects.filter(test=test)
            serializer = QuestionListSerializer(questions, many=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
