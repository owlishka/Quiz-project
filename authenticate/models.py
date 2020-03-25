from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


SEX = (
    ('Man', 'Man'),
    ('Woman', 'Woman'),
    ('Unknown', 'Unknown')
)


class UserProfile(AbstractUser):
    picture = models.ImageField(upload_to='images/', null=True, blank=True, default='images/avatar_2x.png')
    birthday = models.DateTimeField(null=True, blank=True)
    sex = models.CharField(choices=SEX, max_length=10, null=True, default='Unknown')
    info = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('User')
