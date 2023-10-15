from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from apps.users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Введите имя пользователя",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Введите пароль",
    }))

    class Meta:
        model = User
        fields = ("username", "password")


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label="Nickname", widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Введите ник",
    }))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "E@mail.ru",
    }))
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Введите имя",
    }))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Введите фамилию",
    }))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Введите пароль",
    }))
    password2 = forms.CharField(label="Пароль 2", widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Подтвердите пароль",
    }))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "readonly": True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control", "readonly": True}))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")
