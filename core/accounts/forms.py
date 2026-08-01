from django import forms
from django.contrib.auth.forms import(
    AuthenticationForm, UserCreationForm, PasswordChangeForm, SetPasswordForm
)

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["first_name"].error_messages = {
            "required": "نام الزامی است.",
        }
        self.fields["last_name"].error_messages = {
            "required": "نام خانوادگی الزامی است.",
        }
        self.fields["email"].error_messages = {
            "required": "ایمیل الزامی است.",
            "invalid": "ایمیل معتبر وارد کنید.",
            "unique": "کاربری با این ایمیل قبلاً ثبت شده است.",
        }
        self.fields["password1"].error_messages = {
            "required": "رمز عبور الزامی است.",
        }
        self.fields["password2"].error_messages = {
            "required": "تکرار رمز عبور الزامی است.",
        }

        self.error_messages.update({
            "password_mismatch": "دو رمز عبور یکسان نیستند.",
        })


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        error_messages={
            "required": "ایمیل الزامی است.",
            "invalid": "ایمیل معتبر وارد کنید.",
        }
    )
    password = forms.CharField(
        error_messages={
            "required": "رمز عبور الزامی است.",
        }
    )

    error_messages = {
        "invalid_login": "ایمیل یا رمز عبور اشتباه است.",
        "inactive": "این حساب کاربری غیرفعال است.",
    }


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "date_of_birth",
            "avatar",
        )


class PersianPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].error_messages = {
            "required": "رمز عبور فعلی الزامی است.",
        }
        self.fields["new_password1"].error_messages = {
            "required": "رمز عبور جدید الزامی است.",
        }
        self.fields["new_password2"].error_messages = {
            "required": "تکرار رمز جدید الزامی است.",
        }
        self.error_messages.update({
            "password_mismatch": "دو رمز عبور یکسان نیستند.",
            "password_incorrect": "رمز عبور فعلی اشتباه است.",
        })


class PersianSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.update({
            "password_mismatch": "دو رمز عبور یکسان نیستند.",
        })
