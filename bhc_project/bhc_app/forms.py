from django.db.models import fields
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

from django.contrib.auth.forms import PasswordChangeForm
#https://simpleisbetterthancomplex.com/tips/2016/08/04/django-tip-9-password-change-form.html

from django.forms.widgets import DateInput
# https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django

class PatientsRegistration(UserCreationForm):
    class Meta:
        model = Registration
        fields = ['email', 'username', 'password1', 'password2', 'last_name', 'first_name', 'birthday', 'c_number', 'address']
        widgets = {
            'birthday': DateInput(attrs={'type': 'date'}),
        }


