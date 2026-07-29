from django.contrib import admin

from .models import Order, OrderItem, Coupon


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id", "first_name", "last_name", "phone_number",
        "status", "total_price", "created_at"
    )
    list_filter = ("status", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone_number")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "total_price")
    inlines = (OrderItemInline,)

    fieldsets = (
        (
            "Customer",
            {
                "fields": (
                    "user", "first_name", "last_name", "email",
                    "phone_number", "address", "description"
                )
            },
        ),
        (
            "Order",
            {
                "fields": ("status", "total_price")
            },
        ),
        (
            "Dates",
            {
                "fields": ("created_at", "updated_at")
            },
        ),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = ("order", "product", "quantity", "price", "total_price")
    search_fields = ("product__name", "order__id")
    autocomplete_fields = ("order", "product")


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "discount",
        "is_active",
        "valid_from",
        "valid_to",
        "created_at",
    )

    list_filter = (
        "is_active",
        "valid_from",
        "valid_to",
    )

    search_fields = (
        "code",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
