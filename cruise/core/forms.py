from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserModule

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserModule
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)
