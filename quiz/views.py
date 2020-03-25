from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView
from quiz.filters import TestFilter
from quiz.forms import AddTestForm, AddQuizForm, CommentForm
from quiz.models import Test, Question, TestStat, Comment


class IndexTemplateView(TemplateView):
    template_name = 'index.html'


class TestCreateView(CreateView, UserPassesTestMixin):
    """
    User create new Test object.
    """
    http_method_names = ['get', 'post']
    form_class = AddTestForm
    template_name = 'quiz/create_test.html'
    success_url = reverse_lazy('quiz:my_tests')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        request_obj = Test.objects.get(pk=self.kwargs.get('pk'))
        if self.request.user == request_obj.user:
            return True


class MyTestsListView(ListView, UserPassesTestMixin):
    """
    Current user list of tests
    """
    model = Test
    template_name = 'quiz/my_tests.html'
    context_object_name = 'tests'

    def get_queryset(self):
        queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset

    def test_func(self):
        request_obj = Test.objects.get(pk=self.kwargs.get('pk'))
        if self.request.user == request_obj.owner:
            return True


class AllTestsListView(ListView):
    """
    List of all tests with filtering and sorting objects
    """
    model = Test
    template_name = 'quiz/all_tests.html'
    context_object_name = 'tests'
    test_filter = None

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        qs = self.model.objects.filter(is_active=True)
        self.test_filter = TestFilter(self.request.GET, queryset=qs)
        date_sort_str = self.request.GET.get('date')
        passes = self.request.GET.get('passes')
        if date_sort_str:
            queryset = queryset.order_by(date_sort_str)
            return queryset
        if passes is not None:
            teststat = TestStat.objects.filter(has_completed=True)
            if passes == '1':
                return queryset.filter(attempts__in=teststat, owner=self.request.user)
            return queryset.exclude(attempts__in=teststat)
        return self.test_filter.qs

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update({'filter': self.test_filter})
        return context


class TestDetailView(UserPassesTestMixin, DetailView):
    """
    Detail of test for current user with ability to add questions
    """
    model = Test
    template_name = 'quiz/detail_test.html'
    context_object_name = 'test'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update({'questions': self.object.questions.all(),
                        'question_form': AddQuizForm})
        return context

    def test_func(self):
        request_obj = Test.objects.get(pk=self.kwargs.get('pk'))
        if self.request.user == request_obj.owner or self.request.user.is_superuser:
            return True


class DeleteTestView(DeleteView, UserPassesTestMixin):
    model = Test
    http_method_names = ['post']

    def get_success_url(self):
        return reverse_lazy('quiz:my_tests')

    def post(self, request, *args, **kwargs):
        self.queryset = self.get_object()
        self.queryset.delete()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def test_func(self):
        if self.request.user == self.queryset.owner:
            return True


class DeleteCommentView(DeleteView, UserPassesTestMixin):
    model = Comment
    http_method_names = ['post']

    def get_success_url(self, **kwargs):
        return str(self.request.META.get('HTTP_REFERER'))

    def post(self, request, *args, **kwargs):
        self.queryset = self.get_object()
        self.queryset.delete()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def test_func(self):
        if self.request.user == self.queryset.candidate:
            return True


class TestPublicView(DetailView):
    """
    Detail of test for all users with ability to add comments
    """
    model = Test
    template_name = 'quiz/public_detail_test.html'
    context_object_name = 'test'

    def get_context_data(self, object_list=None, **kwargs):
        user_teststat = None
        context = super().get_context_data(object_list=None, **kwargs)
        test = Test.objects.get(pk=self.kwargs.get('pk'))
        if self.request.user.is_authenticated:
            try:
                user_teststat = TestStat.objects.get(test=test, candidate=self.request.user)
            except:
                user_teststat = None
        context.update({'comments': self.object.comments.all(),
                        'comment_form': CommentForm,
                        'user_teststat': user_teststat})
        return context


class CommentCreateView(UserPassesTestMixin, CreateView):
    """
    User create new comment object.
    """
    form_class = CommentForm
    request_obj = None

    def form_valid(self, form):
        form.instance.candidate = self.request.user
        form.instance.test = self.request_obj
        return super().form_valid(form)

    def get_success_url(self):
        return str(self.request.META.get('HTTP_REFERER'))

    def test_func(self):
        self.request_obj = Test.objects.get(pk=self.kwargs.get('pk'))
        return True


class QuestionList(ListView):
    """
    List of all questions
    """
    model = Question
    template_name = 'quiz/take_quiz.html'
    context_object_name = 'questions'

    def get_queryset(self):
        queryset = super().get_queryset().filter(test=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        test = Test.objects.get(pk=self.kwargs.get('pk'))
        num_of_questions = Question.objects.filter(test=self.kwargs.get('pk')).count()
        teststat, created = TestStat.objects.get_or_create(
            test=test, candidate=self.request.user
        )
        has_completed = teststat.has_completed
        if teststat.score:
            score = round(teststat.score, 1)
        else:
            score = 0
        context.update({'num_questions': range(num_of_questions),
                        'score': score,
                        "testno": test.id,
                        "has_completed": has_completed, })
        return context


class EndTestView(UserPassesTestMixin, View):
    request_obj = None

    def post(self, request, *args, **kwargs):
        messages.error(request, 'You finished with that quiz')
        self.request_obj.has_completed = True
        self.request_obj.save()
        return redirect(self.request.META.get('HTTP_REFERER'))

    def test_func(self):
        self.request_obj, created = TestStat.objects.get_or_create(
            test=Test.objects.get(pk=self.kwargs.get('pk')), candidate=self.request.user.id
        )
        return True
