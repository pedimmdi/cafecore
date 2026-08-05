from django.test import TestCase, Client
from django.urls import reverse

from menu.models import Category, Product


class MenuTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="غذای اصلی",
            slug="main-course",
            is_active=True,
        )
        self.product = Product.objects.create(
            category=self.category,
            name="چلوکباب",
            slug="chelo-kebab",
            description="تست",
            price=250000,
            inventory=10,
            is_available=True,
        )

    def test_product_list(self):
        response = self.client.get(reverse("menu:product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "چلوکباب")

    def test_product_detail(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_category_detail(self):
        response = self.client.get(self.category.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.client.get(reverse("menu:search"), {"q": "کباب"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "چلوکباب")
