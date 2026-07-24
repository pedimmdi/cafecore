from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm

from .models import User


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class LoginForm(AuthenticationForm):
    pass


class ProfileUpdateForm(ModelForm):

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
        )
