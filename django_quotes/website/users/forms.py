from django.forms import CharField, TextInput, EmailField, EmailInput, PasswordInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm


class RegisterForm(UserCreationForm):
    username = CharField(
        min_length=5,
        max_length=100,
        required=True,
        widget=TextInput(attrs={
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "Enter your username"}))
    
    first_name = CharField(
        min_length=3,
        max_length=100,
        required=True,
        widget=TextInput(attrs={
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "Enter your first name"}))

    last_name = CharField(
        min_length=3,
        max_length=100,
        required=True,
        widget=TextInput(attrs={
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "Enter your last name"}))

    email = EmailField(
        min_length=5,
        max_length=100,
        required=True,
        widget=EmailInput(attrs={
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "Enter your email"}))

    password1 = CharField(
        max_length=20,
        min_length=8,
        required=True,
        widget=PasswordInput(attrs={
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "Enter your password"}))

    password2 = CharField(
        max_length=20,
        min_length=8,
        required=True,
        widget=PasswordInput(attrs={
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "Confirm your password"}))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = CharField(
        max_length=100,
        required=True,
        widget=TextInput(attrs={
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "Enter your username"}))
    password = CharField(
        max_length=20,
        min_length=6,
        required=True,
        widget=PasswordInput(attrs={
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "Enter your password"}))

    class Meta:
        model = User
        fields = ("username", "password")


class EmailForm(UserCreationForm):
    email = EmailField(
        min_length=5,
        max_length=100,
        required=True,
        widget=EmailInput(attrs={
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "Enter your email"}))

class EmailForm(PasswordResetForm):
    password1 = CharField(
        max_length=20,
        min_length=8,
        required=True,
        widget=PasswordInput(attrs={
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "Enter your password"}))

    password2 = CharField(
        max_length=20,
        min_length=8,
        required=True,
        widget=PasswordInput(attrs={
            "class": "u-border-2 u-input u-input-rectangle u-radius-10",
            "placeholder": "Confirm your password"}))