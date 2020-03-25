from django.contrib import admin
from django.contrib.auth.models import Group

from quiz.models import TestStat
from .models import UserProfile


class ResultInline(admin.TabularInline):
    model = TestStat
    readonly_fields = ('test', 'has_completed', "date_taken", '_score')
    exclude = ('score', )
    extra = 0
    empty_value_display = 'This test still do not completed'

    def _score(self, obj):
        return str(obj.score) + '%'


class UsersAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'email')
    list_display = ('username', 'first_name', 'last_name', 'is_active')
    list_display_links = ('username',)
    search_fields = ('username', 'first_name', )
    inlines = [ResultInline]


admin.site.register(UserProfile, UsersAdmin)
admin.site.unregister(Group)
