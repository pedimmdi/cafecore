from django import forms
from django.utils.text import slugify
from django.utils import timezone

from orders.models import Coupon
from menu.models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "slug", "image", "description", "is_active")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "نام دسته‌بندی"}),
            "slug": forms.TextInput(attrs={"placeholder": "slug-example"}),
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "توضیحات (اختیاری)"}),
            "image": forms.FileInput(attrs={"accept": "image/*"}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug") or ""
        if not slug and self.cleaned_data.get("name"):
            slug = slugify(self.cleaned_data["name"], allow_unicode=True)
        return slug


def _time_choices():
    choices = [("", "انتخاب ساعت")]
    en = "0123456789"
    fa = "۰۱۲۳۴۵۶۷۸۹"
    for h in range(10, 24):
        for m in (0, 30):
            value = f"{h:02d}:{m:02d}"
            label = value.translate(str.maketrans(en, fa))
            choices.append((value, label))
    return choices


TIME_CHOICES = _time_choices()


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "category",
            "name",
            "slug",
            "image",
            "description",
            "ingredients",
            "price",
            "inventory",
            "is_available",
            "is_featured",
            "serving_start",
            "serving_end",
        )
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "نام محصول"}),
            "slug": forms.TextInput(attrs={"placeholder": "slug-example"}),
            "image": forms.FileInput(attrs={"accept": "image/*"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "توضیحات محصول"}),
            "ingredients": forms.Textarea(attrs={"rows": 2, "placeholder": "مواد اولیه (اختیاری)"}),
            "price": forms.NumberInput(attrs={"min": 0, "placeholder": "قیمت به تومان"}),
            "inventory": forms.NumberInput(attrs={"min": 0}),
            "serving_start": forms.Select(choices=TIME_CHOICES, attrs={"class": "time-select"}),
            "serving_end": forms.Select(choices=TIME_CHOICES, attrs={"class": "time-select"}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug") or ""
        if not slug and self.cleaned_data.get("name"):
            slug = slugify(self.cleaned_data["name"], allow_unicode=True)
        return slug


class InventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("inventory", "is_available")
        widgets = {
            "inventory": forms.NumberInput(attrs={"min": 0, "class": "inv-input"}),
        }


class CouponForm(forms.ModelForm):
    valid_from_date = forms.CharField(required=True, widget=forms.HiddenInput())
    valid_from_time = forms.ChoiceField(choices=TIME_CHOICES, required=True)
    valid_to_date = forms.CharField(required=True, widget=forms.HiddenInput())
    valid_to_time = forms.ChoiceField(choices=TIME_CHOICES, required=True)

    class Meta:
        model = Coupon
        fields = ("code", "discount", "max_uses", "once_per_user", "is_active")
        widgets = {
            "code": forms.TextInput(attrs={"placeholder": "مثلاً: NOWROZ1405"}),
            "discount": forms.NumberInput(attrs={"min": 1, "max": 100, "placeholder": "درصد تخفیف"}),
            "max_uses": forms.NumberInput(
                attrs={"min": 1, "placeholder": "خالی = نامحدود"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["max_uses"].required = False
        if self.instance and self.instance.pk:
            vf = self.instance.valid_from
            vt = self.instance.valid_to
            if vf:
                self.fields["valid_from_date"].initial = vf.strftime("%Y-%m-%d")
                self.fields["valid_from_time"].initial = vf.strftime("%H:%M")
            if vt:
                self.fields["valid_to_date"].initial = vt.strftime("%Y-%m-%d")
                self.fields["valid_to_time"].initial = vt.strftime("%H:%M")

    def clean_code(self):
        code = self.cleaned_data.get("code", "").strip().upper()
        if not code:
            raise forms.ValidationError("کد تخفیف الزامی است.")
        qs = Coupon.objects.filter(code__iexact=code)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("این کد قبلاً ثبت شده است.")
        return code

    def clean_discount(self):
        discount = self.cleaned_data.get("discount")
        if discount is None or discount < 1 or discount > 100:
            raise forms.ValidationError("درصد تخفیف باید بین ۱ تا ۱۰۰ باشد.")
        return discount

    def clean_max_uses(self):
        max_uses = self.cleaned_data.get("max_uses")
        if max_uses is not None and max_uses < 1:
            raise forms.ValidationError("سقف استفاده باید حداقل ۱ باشد.")
        return max_uses

    def clean(self):
        from datetime import datetime
        from django.utils import timezone as tz

        cleaned = super().clean()
        try:
            from_dt = datetime.strptime(
                f"{cleaned.get('valid_from_date')} {cleaned.get('valid_from_time')}",
                "%Y-%m-%d %H:%M",
            )
            to_dt = datetime.strptime(
                f"{cleaned.get('valid_to_date')} {cleaned.get('valid_to_time')}",
                "%Y-%m-%d %H:%M",
            )
            if tz.is_naive(from_dt):
                from_dt = tz.make_aware(from_dt)
            if tz.is_naive(to_dt):
                to_dt = tz.make_aware(to_dt)
            cleaned["valid_from"] = from_dt
            cleaned["valid_to"] = to_dt
            if to_dt <= from_dt:
                raise forms.ValidationError("تاریخ پایان باید بعد از تاریخ شروع باشد.")
        except (TypeError, ValueError):
            raise forms.ValidationError("تاریخ یا ساعت نامعتبر است.")
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.valid_from = self.cleaned_data["valid_from"]
        instance.valid_to = self.cleaned_data["valid_to"]
        if commit:
            instance.save()
        return instance
