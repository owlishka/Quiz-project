from django.contrib import admin
from django.urls import path, include
from quiz.views import IndexTemplateView
from test_platform import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('quiz/', include(('quiz.urls', 'quiz'))),
    path('authenticate/', include(('authenticate.urls', 'authenticate'))),
    path('user/', include(('accounts.urls', 'user'))),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
