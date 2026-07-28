from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    ordering = ("-created_at",)
    list_display = (
        "order", "authority", "amount", "status", "created_at"
    )
    list_filter = ("status", "created_at")
    search_fields = (
        "authority", "ref_id", "order__id", "order__user__email"
    )
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (

        (
            "Payment Information",
            {
                "fields": (
                    "order", "authority", "ref_id", "amount", "status"
                ),
            },
        ),

        (
            "Dates",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),

    )
