from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser


#register from specified here with custom fields
class RegisterForm(UserCreationForm):
    email=forms.EmailField(required=True,help_text="Ex. xyz@abc.com",widget=forms.EmailInput(attrs={'class':'common-input mt-20'}))
    password1=forms.CharField(required=True,help_text='',label="Password",widget=forms.PasswordInput(attrs={'class':'common-input'}))
    password2=forms.CharField(required=True,help_text='',label="Password Confirmation",widget=forms.PasswordInput(attrs={'class':'common-input mt-20'}))
    class Meta:
        model=CustomUser
        fields=['email','password1','password2']

