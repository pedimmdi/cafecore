from django.test import TestCase, Client
from django.urls import reverse


class PagesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home(self):
        self.assertEqual(self.client.get(reverse("pages:home")).status_code, 200)

    def test_about(self):
        self.assertEqual(self.client.get(reverse("pages:about")).status_code, 200)

    def test_contact(self):
        self.assertEqual(self.client.get(reverse("pages:contact")).status_code, 200)
