from django.db import models


class SiteSettings(models.Model):

    site_name = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    logo = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
    )

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=20,
    )

    address = models.TextField()

    working_hours = models.CharField(
        max_length=255,
    )

    instagram = models.URLField(
        blank=True,
    )

    telegram = models.URLField(
        blank=True,
    )

    whatsapp = models.URLField(
        blank=True,
    )

    linkedin = models.URLField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = (
            "-created_at",
        )

    def __str__(self):

        return self.site_name
