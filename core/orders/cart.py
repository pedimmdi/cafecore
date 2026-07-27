from decimal import Decimal

from menu.models import Product


class Cart:

    SESSION_KEY = "cart"

    def __init__(self, request):

        self.session = request.session

        cart = self.session.get(self.SESSION_KEY)

        if cart is None:

            cart = self.session[self.SESSION_KEY] = {}

        self.cart = cart

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

            self.save()

    def __len__(self):

        return sum(

            item["quantity"]

            for item in self.cart.values()

        )

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

            item["total_price"] = (
                item["price"] * item["quantity"]
            )

            yield item

    def get_total_price(self):

        return sum(

            Decimal(item["price"]) * item["quantity"]

            for item in self.cart.values()

        )

    def is_empty(self):

        return len(self.cart) == 0
