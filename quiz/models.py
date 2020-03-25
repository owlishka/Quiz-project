import bleach
from django.db import models
from django.urls import reverse
from authenticate.models import UserProfile


class Test(models.Model):
    name = models.CharField(max_length=100, blank=False, default="Sample Test")
    description = models.TextField(max_length=500, null=True, blank=True)
    owner = models.ForeignKey(
        UserProfile, related_name="tests", null=True, on_delete=models.SET_NULL
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    published_on = models.DateTimeField(null=True)

    def score(self):
        return self.attempts.all()

    def get_attempts(self):
        return self.attempts.all().count()

    def get_question_count(self):
        return self.questions.all().count()

    def get_absolute_url(self):
        return reverse("quiz:detail_test", args=[self.id])

    def get_test_detail_url(self):
        return reverse("quiz:detail_public_test", args=[self.id])

    def __str__(self):
        return self.name


class Question(models.Model):
    test = models.ForeignKey(Test, related_name="questions", on_delete=models.CASCADE)
    question = models.TextField(max_length=2000, blank=False)
    wrong_answer_1 = models.CharField(max_length=500, blank=False, null=False)
    wrong_answer_2 = models.CharField(max_length=500, blank=True, null=True)
    wrong_answer_3 = models.CharField(max_length=500, blank=True, null=True)
    correct_answer = models.CharField(max_length=500, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def get_update_url(self):
        return reverse(
            "quiz:update_question", kwargs={"tpk": self.test.id, "qpk": self.id}
        )

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = 'Questions'
        ordering = ['-created_on']


class TestStat(models.Model):
    test = models.ForeignKey(
        Test, related_name="attempts", null=True, on_delete=models.SET_NULL
    )
    candidate = models.ForeignKey(
        UserProfile, related_name="teststats", on_delete=models.CASCADE
    )
    has_completed = models.BooleanField(default=False)
    date_taken = models.DateTimeField(auto_now_add=True)
    score = models.DecimalField(max_digits=9, decimal_places=2, null=True)

    def get_total_attempts(self):
        return QuestionStat.objects.filter(
            question__in=self.test.questions.all(), candidate=self.candidate
        ).count()

    def get_wrong_response_count(self):
        if self.has_completed:
            return (
                QuestionStat.objects.filter(
                    question__in=self.test.questions.all(),
                    candidate=self.candidate,
                    is_correct=False,
                    response__isnull=False,
                )
                    .exclude(response__exact="")
                    .count()
            )
        return None

    def get_correct_response_count(self):
        if self.has_completed:
            return QuestionStat.objects.filter(
                question__in=self.test.questions.all(),
                candidate=self.candidate,
                is_correct=True,
            ).count()
        return None

    def save(self, *args, **kwargs):
        if self.has_completed:
            self.score = (QuestionStat.objects.filter(
                question__in=self.test.questions.all(),
                candidate=self.candidate,
                is_correct=True,
            ).count() / self.test.questions.all().count() * 100)
        super(TestStat, self).save(*args, **kwargs)

    def __str__(self):
        return "{}-{}".format(self.test, "Stat")


class QuestionStat(models.Model):
    question = models.ForeignKey(
        Question, related_name="question_history", null=True, on_delete=models.SET_NULL
    )
    candidate = models.ForeignKey(
        UserProfile, related_name="questionstat", null=True, on_delete=models.CASCADE
    )
    response = models.CharField(max_length=500, blank=True)
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.response == bleach.clean(self.question.correct_answer):
            self.is_correct = True
        super(QuestionStat, self).save(*args, **kwargs)

    # def __str__(self):
    #     return "{}-{}".format(self.question.question, "stat")


class Comment(models.Model):
    test = models.ForeignKey(Test, related_name="comments", on_delete=models.CASCADE)
    candidate = models.ForeignKey(
        UserProfile, related_name="candidate_comments", on_delete=models.CASCADE
    )
    message = models.CharField(max_length=2000)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
