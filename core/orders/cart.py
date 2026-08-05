from decimal import Decimal

from menu.models import Product

from .models import Coupon


class Cart:

    SESSION_KEY = "cart"

    def __init__(self, request):
        self.request = request
        self.session = request.session

        cart = self.session.get(self.SESSION_KEY)
        if cart is None:
            cart = self.session[self.SESSION_KEY] = {}

        self.cart = cart
        self.coupon_id = self.session.get("coupon_id")

    def save(self):
        self.session.modified = True

    def add(self, product, quantity=1, override_quantity=False):
        if not product.is_available:
            return False
        if product.inventory <= 0:
            return False

        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
            }

        current_quantity = self.cart[product_id]["quantity"]

        if override_quantity:
            new_quantity = quantity
        else:
            new_quantity = current_quantity + quantity

        if new_quantity > product.inventory:
            new_quantity = product.inventory

        self.cart[product_id]["quantity"] = new_quantity
        self.save()
        return True

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            return

        if quantity <= 0:
            del self.cart[product_id]
            self.save()
            return

        if quantity > product.inventory:
            quantity = product.inventory

        self.cart[product_id]["quantity"] = quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        if self.SESSION_KEY in self.session:
            del self.session[self.SESSION_KEY]
        self.clear_coupon()
        self.save()

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(
            id__in=product_ids,
            is_available=True,
        )
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            if "product" not in item:
                continue
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    @property
    def coupon(self):
        if not self.coupon_id:
            return None
        try:
            coupon = Coupon.objects.get(id=self.coupon_id)
        except Coupon.DoesNotExist:
            return None

        user = getattr(self.request, "user", None)
        if user is not None and not getattr(user, "is_authenticated", False):
            user = None

        if coupon.is_usable(user=user):
            return coupon
        return None

    def get_discount(self):
        if self.coupon:
            return (
                self.get_total_price()
                * Decimal(self.coupon.discount)
                / Decimal("100")
            )
        return Decimal("0")

    def get_final_price(self):
        return self.get_total_price() - self.get_discount()

    def clear_coupon(self):
        self.session.pop("coupon_id", None)
        self.coupon_id = None
        self.save()

    def is_empty(self):
        return len(self.cart) == 0
