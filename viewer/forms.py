from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields, ModelForm, models
from django.core.exceptions import ValidationError
from viewer.models import UserGifs

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class GifsSearch(ModelForm):

    class Meta:
        model = UserGifs
        fields = '__all__'
