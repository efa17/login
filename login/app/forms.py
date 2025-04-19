from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email', 'phone', 'password']

class LoginForm(forms.Form):
    email_or_phone = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
