from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ("-created_at",)
    search_fields = ("email", "first_name", "last_name")
    list_display = (
        "email", "first_name", "last_name",
        "is_active", "is_staff", "last_login", "created_at"
    )
    list_filter = ("is_active", "is_staff", "is_superuser")
    readonly_fields = ("created_at", "updated_at", "last_login")
    list_per_page = 25

    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("email", "password")
            },
        ),
        (
            "Personal Information",
            {
                "fields": ("first_name", "last_name")
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active", "is_staff", "is_superuser",
                    "groups", "user_permissions"
                )
            },
        ),
        (
            "Important Dates",
            {
                "fields": ("last_login", "created_at", "updated_at")
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                  "email", "first_name", "last_name",
                  "password1", "password2", "is_active", "is_staff"  
                ),
            },
        ),
    )
