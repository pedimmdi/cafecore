from django.conf import settings
from django.db import models


class Reservation(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار"
        CONFIRMED = "confirmed", "تأیید شده"
        CANCELLED = "cancelled", "لغو شده"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="reservations"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    number_of_guests = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = [
            "-reservation_date",
            "-reservation_time",
        ]

    def __str__(self):

        return (
            f"{self.first_name} "
            f"{self.last_name} - "
            f"{self.reservation_date}"
        )
