from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import User


class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="user@test.com",
            password="TestPass123!",
            first_name="علی",
            last_name="تست",
        )

    def test_create_user(self):
        self.assertEqual(self.user.email, "user@test.com")
        self.assertTrue(self.user.check_password("TestPass123!"))
        self.assertFalse(self.user.is_staff)

    def test_login_page(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        logged_in = self.client.login(
            email="user@test.com",
            password="TestPass123!",
        )
        self.assertTrue(logged_in)

    def test_profile_requires_login(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 302)

    def test_profile_authenticated(self):
        self.client.login(email="user@test.com", password="TestPass123!")
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 200)
