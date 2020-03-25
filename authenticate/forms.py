from django import forms
from django.contrib.auth.forms import UserCreationForm
from authenticate.models import UserProfile


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    birthday = forms.DateField(widget=forms.TextInput(attrs=
    {
        'class': 'datepicker'
    }))

    class Meta:
        model = UserProfile
        fields = ('username', 'password1', 'password2', 'sex', 'first_name', 'last_name', 'email', 'birthday')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2', 'sex']:
            self.fields[fieldname].help_text = None

