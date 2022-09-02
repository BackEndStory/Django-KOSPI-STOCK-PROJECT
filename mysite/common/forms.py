from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import django.contrib.auth.forms as auth_forms


class UserForm(UserCreationForm):
    email = forms.EmailField(label="email")
    username = forms.CharField(label="ID")
    first_name = forms.CharField(label="name")

    class Meta:
        model = User
        fields = ("username", "first_name", "password1", "email" )




