from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Interest,ChatMessage

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ['receiver', 'message']
        widgets = {
            'receiver': forms.HiddenInput(),
            'message': forms.Textarea(attrs={'rows': 3}),
        }

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['receiver', 'message']
        widgets = {
            'receiver': forms.HiddenInput(),
            'message': forms.Textarea(attrs={'rows': 3}),
        }