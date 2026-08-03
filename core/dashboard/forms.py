from django import forms
from django.utils.text import slugify

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
