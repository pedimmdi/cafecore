from django.conf import settings
from django.db import models

from menu.models import Product


class Review(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار"
        APPROVED = "approved", "تأیید شده"
        REJECTED = "rejected", "رد شده"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.PositiveSmallIntegerField()

    comment = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
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

        constraints = (
            models.UniqueConstraint(
                fields=[
                    "user",
                    "product",
                ],
                name="unique_review_per_user_product",
            ),
        )

    def __str__(self):

        return f"{self.user.email} - {self.product.name}"
