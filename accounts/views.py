from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, RedirectView, UpdateView
from social_django.models import UserSocialAuth

from authenticate.models import UserProfile


class UserHomeRedirectView(RedirectView):
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        user = get_object_or_404(UserProfile, pk=self.request.user.id)
        return reverse('user:my_profile', kwargs={'pk': user.pk, 'username': user.username})


class ProfileView(DetailView):
    model = UserProfile
    template_name = 'Authenticate/profile.html'
    context_object_name = 'users'
    slug_field = 'username'


class ProfileUpdateView(UpdateView, UserPassesTestMixin):
    model = UserProfile
    template_name = 'Authenticate/update_profile.html'
    success_url = reverse_lazy('user:redirect')
    fields = ['first_name', 'last_name', 'birthday', 'info', 'sex', 'picture', 'email']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        user = self.request.user

        try:
            github_login = user.social_auth.get(provider='github')
        except UserSocialAuth.DoesNotExist:
            github_login = None

        try:
            twitter_login = user.social_auth.get(provider='twitter')
        except UserSocialAuth.DoesNotExist:
            twitter_login = None

        can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

        context.update({'github_login': github_login,
                        'twitter_login': twitter_login,
                        'can_disconnect': can_disconnect})
        return context

    def test_func(self):
        request_obj = UserProfile.objects.get(pk=self.kwargs.get('pk'))
        if self.request.user == request_obj.user:
            return True



