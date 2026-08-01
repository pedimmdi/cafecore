from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import (
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
    UserAttributeSimilarityValidator,
)


class PersianMinimumLengthValidator(MinimumLengthValidator):
    def __init__(self, min_length=8):
        super().__init__(min_length=min_length)

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                f"رمز عبور باید حداقل {self.min_length} کاراکتر باشد.",
                code="password_too_short",
            )

    def get_help_text(self):
        return f"رمز عبور باید حداقل {self.min_length} کاراکتر باشد."


class PersianCommonPasswordValidator(CommonPasswordValidator):
    def validate(self, password, user=None):
        try:
            super().validate(password, user)
        except ValidationError:
            raise ValidationError(
                "این رمز عبور خیلی ساده و رایج است.",
                code="password_too_common",
            )

    def get_help_text(self):
        return "رمز عبور نباید از رمزهای رایج باشد."


class PersianNumericPasswordValidator(NumericPasswordValidator):
    def validate(self, password, user=None):
        try:
            super().validate(password, user)
        except ValidationError:
            raise ValidationError(
                "رمز عبور نمی‌تواند فقط عدد باشد.",
                code="password_entirely_numeric",
            )

    def get_help_text(self):
        return "رمز عبور نمی‌تواند فقط عدد باشد."


class PersianUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def validate(self, password, user=None):
        try:
            super().validate(password, user)
        except ValidationError:
            raise ValidationError(
                "رمز عبور شباهت زیادی به اطلاعات شخصی شما دارد.",
                code="password_too_similar",
            )

    def get_help_text(self):
        return "رمز عبور نباید شبیه نام یا ایمیل شما باشد."