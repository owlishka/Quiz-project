from django.conf.urls import include, url
from django.urls import path
from rest_framework.authtoken import views
from authenticate.views import Login, Register, Logout, social_password
from test_platform import settings


urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('oauth/', include('social_django.urls', namespace="social")),
    url('settings/password/', social_password, name='password'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )