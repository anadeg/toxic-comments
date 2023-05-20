from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    # email = forms.EmailField(required=True)
    username = forms.CharField(label='Name',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Password Confirmation',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-input'}),
            "password1": forms.TextInput(attrs={'class': 'form-input'}),
            "password2": forms.TextInput(attrs={'class': 'form-input'})
        }
