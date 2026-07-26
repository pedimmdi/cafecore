from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {
                "fields": ("name", "slug", "image", "description")
            },
        ),
        (
            "Status",
            {
                "fields": ("is_active",)
            },
        ),
        (
            "Dates",
            {
                "fields": ("created_at", "updated_at")
            },
        ),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name", "category", "price", "inventory",
        "is_available", "is_featured", "created_at"
    )
    list_filter = ("category", "is_available", "is_featured", "created_at")
    search_fields = ("name", "description", "ingredients")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("category",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "category", "name", "slug",
                    "image", "description", "ingredients"
                )
            },
        ),
        (
            "Pricing",
            {
                "fields": ("price", "inventory")
            },
        ),
        (
            "Availability",
            {
                "fields": (
                    "is_available", "is_featured", "serving_start", "serving_end"
                )
            },
        ),
        (
            "Dates",
            {
                "fields": ("created_at", "updated_at")
            },
        ),
    )
