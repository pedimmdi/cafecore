from datetime import date, time, timedelta

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from reservations.models import Reservation


class ReservationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="guest@test.com",
            password="TestPass123!",
            first_name="مهمان",
            last_name="تست",
            phone_number="09120000000",
        )

    def test_create_page_requires_login(self):
        response = self.client.get(reverse("reservations:create"))
        self.assertEqual(response.status_code, 302)

    def test_create_page_authenticated(self):
        self.client.login(email="guest@test.com", password="TestPass123!")
        response = self.client.get(reverse("reservations:create"))
        self.assertEqual(response.status_code, 200)

    def test_create_reservation(self):
        self.client.login(email="guest@test.com", password="TestPass123!")
        future = timezone.localdate() + timedelta(days=3)
        response = self.client.post(
            reverse("reservations:create"),
            {
                "first_name": "مهمان",
                "last_name": "تست",
                "email": "guest@test.com",
                "phone_number": "09120000000",
                "reservation_date": future.isoformat(),
                "reservation_time": "19:00",
                "number_of_guests": 4,
                "description": "نزدیک پنجره",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Reservation.objects.filter(
                user=self.user,
                number_of_guests=4,
                status=Reservation.Status.PENDING,
            ).exists()
        )

    def test_guests_over_limit_rejected(self):
        self.client.login(email="guest@test.com", password="TestPass123!")
        future = timezone.localdate() + timedelta(days=3)
        response = self.client.post(
            reverse("reservations:create"),
            {
                "first_name": "مهمان",
                "last_name": "تست",
                "email": "guest@test.com",
                "phone_number": "09120000000",
                "reservation_date": future.isoformat(),
                "reservation_time": "19:00",
                "number_of_guests": 25,
                "description": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reservation.objects.count(), 0)
