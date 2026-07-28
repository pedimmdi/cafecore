from django.db import models

from orders.models import Order


class Payment(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payment"
    )
    authority = models.CharField(max_length=150, unique=True)
    ref_id = models.CharField(max_length=150, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.authority
