from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserModule

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserModule
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        # Save the user instance
        user = super().save(commit=False)
        
        # Set the role to 'customer' by default
        user.role = 'customer'
        
        if commit:
            user.save()  # Save the user to the database
        return user

class LoginForm(forms.Form):
    username = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)
