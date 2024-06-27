from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import StdProfile,Marks,Subject,Notice


class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'email','username','password1','password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    error_messages={
            'required': 'Please enter your username.',
            'max_length': 'Username cannot exceed 150 characters.'
    }
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    error_messages={
            'required': 'Please enter your password.'
        }

class StdProfileForm(forms.ModelForm):
    class Meta:
        model = StdProfile
        fields = ['department', 'semester','course', 'gender','roll_number']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'department','semester','course']

class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['student', 'subject', 'marks']


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']