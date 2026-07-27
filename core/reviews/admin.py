from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    ordering = (
        "-created_at",
    )

    list_display = (
        "product",
        "user",
        "rating",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "rating",
        "created_at",
    )

    search_fields = (
        "user__email",
        "product__name",
        "comment",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Review",
            {
                "fields": (
                    "user",
                    "product",
                    "rating",
                    "comment",
                    "status",
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
