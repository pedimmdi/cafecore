from django.contrib import admin

from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "site_name",
        "email",
        "phone_number",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "اطلاعات اصلی",
            {
                "fields": (
                    "site_name",
                    "description",
                    "logo",
                )
            }
        ),

        (
            "اطلاعات تماس",
            {
                "fields": (
                    "email",
                    "phone_number",
                    "address",
                    "working_hours",
                )
            }
        ),

        (
            "شبکه‌های اجتماعی",
            {
                "fields": (
                    "instagram",
                    "telegram",
                    "whatsapp",
                    "linkedin",
                )
            }
        ),

        (
            "تاریخ‌ها",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),

    )

    def has_add_permission(self, request):

        return not SiteSettings.objects.exists()
