from API.models import Task
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
class addTaskForm(ModelForm):

    class Meta:
        model=Task
        fields=('name','description','user',)

class loginform(AuthenticationForm):
    class Meta:
        model=User
        fields=('username','password',)
from django import forms
class RegistrationForm(UserCreationForm):
    # phone=forms.CharField(max_length=10)
    class Meta:
        model=User
        fields=('username','email','password1','password2',)