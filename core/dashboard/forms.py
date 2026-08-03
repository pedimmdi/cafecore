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
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug") or ""
        if not slug and self.cleaned_data.get("name"):
            slug = slugify(self.cleaned_data["name"], allow_unicode=True)
        return slug


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
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "توضیحات محصول"}),
            "ingredients": forms.Textarea(attrs={"rows": 2, "placeholder": "مواد اولیه (اختیاری)"}),
            "price": forms.NumberInput(attrs={"min": 0, "placeholder": "قیمت به تومان"}),
            "inventory": forms.NumberInput(attrs={"min": 0}),
            "serving_start": forms.TimeInput(attrs={"type": "time"}),
            "serving_end": forms.TimeInput(attrs={"type": "time"}),
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
    class Meta:
        model = Coupon
        fields = ("code", "discount", "is_active", "valid_from", "valid_to")
        widgets = {
            "code": forms.TextInput(attrs={"placeholder": "مثلاً: NOWROZ1405"}),
            "discount": forms.NumberInput(attrs={"min": 1, "max": 100, "placeholder": "درصد تخفیف"}),
            "valid_from": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "valid_to": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # نمایش datetime برای input type=datetime-local
        for field_name in ("valid_from", "valid_to"):
            value = self.initial.get(field_name) or getattr(self.instance, field_name, None)
            if value:
                self.initial[field_name] = value.strftime("%Y-%m-%dT%H:%M")

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

    def clean(self):
        cleaned = super().clean()
        valid_from = cleaned.get("valid_from")
        valid_to = cleaned.get("valid_to")
        if valid_from and valid_to and valid_to <= valid_from:
            raise forms.ValidationError("تاریخ پایان باید بعد از تاریخ شروع باشد.")
        return cleaned

