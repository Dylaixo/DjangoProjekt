from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Imie', max_length=100)
    last_name = forms.CharField(label='Nazwisko', max_length=100)
    class Meta:
        model = get_user_model()
        fields = ["username", 'first_name', 'last_name', "password1", "password2"]
