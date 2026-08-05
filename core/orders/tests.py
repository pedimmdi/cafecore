from decimal import Decimal
from datetime import timedelta

from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.utils import timezone

from menu.models import Category, Product
from orders.cart import Cart
from orders.models import Coupon


class CartTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.category = Category.objects.create(name="نوشیدنی", slug="drinks")
        self.product = Product.objects.create(
            category=self.category,
            name="لاته",
            slug="latte",
            description="قهوه",
            price=80000,
            inventory=5,
            is_available=True,
        )

    def _cart(self):
        request = self.factory.get("/")
        request.session = self.client.session
        return Cart(request)

    def test_add_to_cart(self):
        cart = self._cart()
        self.assertTrue(cart.add(self.product, quantity=2))
        self.assertEqual(len(cart), 2)
        self.assertEqual(cart.get_total_price(), Decimal("160000"))

    def test_cannot_exceed_inventory(self):
        cart = self._cart()
        cart.add(self.product, quantity=10)
        self.assertEqual(len(cart), 5)

    def test_remove_from_cart(self):
        cart = self._cart()
        cart.add(self.product, quantity=1)
        cart.remove(self.product)
        self.assertTrue(cart.is_empty())

    def test_unavailable_product_not_added(self):
        self.product.is_available = False
        self.product.save()
        cart = self._cart()
        self.assertFalse(cart.add(self.product, quantity=1))
        self.assertTrue(cart.is_empty())

    def test_coupon_discount(self):
        coupon = Coupon.objects.create(
            code="OFF10",
            discount=10,
            is_active=True,
            valid_from=timezone.now() - timedelta(days=1),
            valid_to=timezone.now() + timedelta(days=30),
        )
        cart = self._cart()
        cart.add(self.product, quantity=1)
        cart.session["coupon_id"] = coupon.id
        cart.coupon_id = coupon.id
        self.assertEqual(cart.get_discount(), Decimal("8000"))
        self.assertEqual(cart.get_final_price(), Decimal("72000"))

    def test_inactive_coupon_gives_no_discount(self):
        coupon = Coupon.objects.create(
            code="DEAD",
            discount=50,
            is_active=False,
            valid_from=timezone.now() - timedelta(days=1),
            valid_to=timezone.now() + timedelta(days=30),
        )
        cart = self._cart()
        cart.add(self.product, quantity=1)
        cart.session["coupon_id"] = coupon.id
        cart.coupon_id = coupon.id
        self.assertIsNone(cart.coupon)
        self.assertEqual(cart.get_discount(), Decimal("0"))

    def test_apply_valid_coupon_via_view(self):
        Coupon.objects.create(
            code="SAVE10",
            discount=10,
            is_active=True,
            valid_from=timezone.now() - timedelta(days=1),
            valid_to=timezone.now() + timedelta(days=30),
        )
        response = self.client.post(
            reverse("orders:coupon_apply"),
            {"code": "SAVE10"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("coupon_id", self.client.session)

    def test_apply_invalid_coupon_via_view(self):
        response = self.client.post(
            reverse("orders:coupon_apply"),
            {"code": "NOPE"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotIn("coupon_id", self.client.session)

    def test_cart_page(self):
        response = self.client.get(reverse("orders:cart"))
        self.assertEqual(response.status_code, 200)
