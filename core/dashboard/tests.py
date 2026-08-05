from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import User


class DashboardAccessTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="user@test.com",
            password="TestPass123!",
            first_name="کاربر",
            last_name="عادی",
        )
        self.staff = User.objects.create_user(
            email="admin@test.com",
            password="AdminPass123!",
            first_name="مدیر",
            last_name="سیستم",
            is_staff=True,
        )

    def test_dashboard_requires_staff(self):
        self.client.login(email="user@test.com", password="TestPass123!")
        response = self.client.get(reverse("dashboard:index"))
        self.assertIn(response.status_code, (302, 403))

    def test_dashboard_staff_ok(self):
        self.client.login(email="admin@test.com", password="AdminPass123!")
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)

    def test_orders_page_staff(self):
        self.client.login(email="admin@test.com", password="AdminPass123!")
        response = self.client.get(reverse("dashboard:orders"))
        self.assertEqual(response.status_code, 200)
