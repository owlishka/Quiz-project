from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AdminPasswordChangeForm, UserModel
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from social_django.models import UserSocialAuth

from authenticate.forms import RegisterForm
from authenticate.models import UserProfile
from rest_framework.authtoken.models import Token


class Login(LoginView):
    http_method_names = ['get', 'post']
    redirect_authenticated_user = True
    template_name = 'Authenticate/login.html'


class Logout(LogoutView):
    http_method_names = ['get']
    template_name = 'Authenticate/logout.html'

    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        return redirect('quiz:index')


class Register(CreateView):
    model = UserProfile
    form_class = RegisterForm
    template_name = 'Authenticate/register.html'
    success_url = reverse_lazy('authenticate:login')

    def form_valid(self, form):
        self.object = form.save()
        Token.objects.create(user=self.object)
        return HttpResponseRedirect(self.get_success_url())


@login_required
def social_password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user:redirect')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'Authenticate/password.html', {'form': form})
