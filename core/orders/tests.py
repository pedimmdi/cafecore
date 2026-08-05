from decimal import Decimal

from django.test import TestCase, RequestFactory

from menu.models import Category, Product
from orders.cart import Cart
from orders.models import Coupon
from django.utils import timezone
from datetime import timedelta


class CartTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
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
