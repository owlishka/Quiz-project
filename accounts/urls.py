from django.urls import path
from accounts.views import ProfileView, UserHomeRedirectView, ProfileUpdateView


urlpatterns = [
    path('<int:pk>/<slug:username>/', ProfileView.as_view(), name='my_profile'),
    path('update/<int:pk>/<slug:username>/', ProfileUpdateView.as_view(), name='update_profile'),
    path('redirect', UserHomeRedirectView.as_view(), name='redirect')
]