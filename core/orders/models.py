from django.conf import settings
from django.db import models

from menu.models import Product


class Coupon(models.Model):

    code = models.CharField(
        max_length=50,
        unique=True,
    )

    discount = models.PositiveSmallIntegerField()

    is_active = models.BooleanField(
        default=True,
    )

    valid_from = models.DateTimeField()

    valid_to = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.code


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار"
        PAID = "paid", "پرداخت شده"
        CANCELLED = "cancelled", "لغو شده"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="orders"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, null=True, blank=True
    )
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk}"

    @property
    def total_price(self):
        return sum(
            item.total_price
            for item in self.items.all()
        )


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.product.name

    @property
    def total_price(self):
        return self.quantity * self.price
