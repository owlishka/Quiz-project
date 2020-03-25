from django.contrib import admin
from quiz.models import Question, Test, TestStat, QuestionStat, Comment


class TestStatAdmin(admin.ModelAdmin):
    list_display = ('test', 'candidate', 'has_completed', 'score')
    list_display_links = ('test', 'candidate')
    search_fields = ('candidate', 'test', )


class TestAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'description', 'is_active', 'published_on')
    list_display_links = ('name', )
    search_fields = ('name', )


admin.site.register(Question)
admin.site.register(Test, TestAdmin)
admin.site.register(TestStat, TestStatAdmin)
admin.site.register(QuestionStat)
admin.site.register(Comment)

