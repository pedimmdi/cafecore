from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "name", "email", "subject", "is_read", "created_at"
    )
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    
    fieldsets = (

        (
            "Message Information",
            {
                "fields": (
                    "name",
                    "email",
                    "subject",
                    "message",
                ),
            },
        ),

        (
            "Status",
            {
                "fields": (
                    "is_read",
                ),
            },
        ),

        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),

    )
