from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext

from user.validators import isnt_totally_dumb_password


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label=ugettext("Password"), widget=forms.PasswordInput, min_length=6, validators=[isnt_totally_dumb_password])
