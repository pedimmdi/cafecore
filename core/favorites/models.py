from django.conf import settings
from django.db import models

from menu.models import Product


class Favorite(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="favorited_by",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = (
            "-created_at",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "user",
                    "product",
                ),
                name="unique_user_favorite_product",
            ),
        ]

    def __str__(self):

        return f"{self.user.email} - {self.product.name}"
