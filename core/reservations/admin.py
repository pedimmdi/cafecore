from django.contrib import admin

from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    ordering = ("-reservation_date", "-reservation_time")
    list_display = (
        "first_name", "last_name", "reservation_date",
        "reservation_time", "number_of_guests", "status", "created_at"
    )
    list_filter = ("status", "reservation_date", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone_number")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (

        (
            "Customer Information",
            {
                "fields": (
                    "user", "first_name", "last_name",
                    "email", "phone_number"
                )
            },
        ),

        (
            "Reservation",
            {
                "fields": (
                    "reservation_date", "reservation_time",
                    "number_of_guests", "description", "status"
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
