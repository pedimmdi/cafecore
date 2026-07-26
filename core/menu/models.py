from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "menu:category_detail",
            kwargs={"slug": self.slug},
        )


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    description = models.TextField()
    ingredients = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    inventory = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    serving_start = models.TimeField(blank=True, null=True)
    serving_end = models.TimeField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_available"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "menu:product_detail",
            kwargs={"slug": self.slug},
        )
