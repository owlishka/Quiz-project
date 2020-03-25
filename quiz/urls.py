from django.urls import path

from quiz.api.resourses import getQuestionList, QuestionStatForm, ScoreChart, UpdateQuestionForm, ToggleTestActive,\
    AddQuestionForm
from quiz.views import MyTestsListView, AllTestsListView, TestDetailView, TestCreateView, \
    DeleteTestView, TestPublicView, CommentCreateView, QuestionList, EndTestView, DeleteCommentView


urlpatterns = [
    path('mytests/', MyTestsListView.as_view(), name='my_tests'),
    path('alltests/', AllTestsListView.as_view(), name='all_tests'),
    path('create/test', TestCreateView.as_view(), name='create_test'),
    path('create/comment/<int:pk>/', CommentCreateView.as_view(), name='create_comment'),
    path('delete/test/<int:pk>/', DeleteTestView.as_view(), name='delete_test'),
    path('delete/comment/<int:pk>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('detail/<int:pk>/', TestDetailView.as_view(), name='detail_test'),
    path('detail/public/<int:pk>/', TestPublicView.as_view(), name='detail_public_test'),
    path('<int:pk>/endquiz', EndTestView.as_view(), name='end_quiz'),
    path('take/<int:pk>/', QuestionList.as_view(), name='take_quiz'),
    path('ajax/<int:pk>/questions', getQuestionList.as_view(), name="getQuestions"),
    path("ajax/<int:qpk>/response", QuestionStatForm.as_view(), name="QuestionStatForm"),
    path("ajax/<int:pk>/add", AddQuestionForm.as_view(), name="addQuestionForm"),
    path("ajax/test/<int:pk>/score_chart", ScoreChart.as_view(), name="score_chart"),
    path('ajax/<int:tpk>/update/question/<int:qpk>', UpdateQuestionForm.as_view(), name='update_question'),
    path('ajax/<int:pk>/activate', ToggleTestActive.as_view(), name='activate_quiz'),
]