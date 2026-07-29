from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import View
from django.utils import timezone

from menu.models import Product

from .cart import Cart
from .forms import CheckoutForm, CouponApplyForm
from .models import Order, OrderItem, Coupon


class CartDetailView(TemplateView):

    template_name = "orders/cart.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["cart"] = Cart(self.request)

        return context


class CartAddView(View):

    def post(self, request, product_id):

        cart = Cart(request)

        product = get_object_or_404(
            Product,
            id=product_id,
            is_available=True,
        )

        try:

            quantity = int(
                request.POST.get(
                    "quantity",
                    1,
                )
            )

        except (TypeError, ValueError):

            quantity = 1

        if quantity < 1:

            quantity = 1

        added = cart.add(
            product=product,
            quantity=quantity,
        )

        if added:

            messages.success(
                request,
                "Product added to cart successfully.",
            )

        else:

            messages.error(
                request,
                "This product is currently unavailable.",
            )

        return redirect(
            "orders:cart",
        )


class CartUpdateView(View):

    def post(self, request, product_id):

        cart = Cart(request)

        product = get_object_or_404(
            Product,
            id=product_id,
        )

        try:

            quantity = int(
                request.POST.get(
                    "quantity",
                    1,
                )
            )

        except (TypeError, ValueError):

            quantity = 1

        cart.update(
            product=product,
            quantity=quantity,
        )

        messages.success(
            request,
            "Cart updated successfully.",
        )

        return redirect(
            "orders:cart",
        )


class CartRemoveView(View):

    def post(self, request, product_id):

        cart = Cart(request)

        product = get_object_or_404(
            Product,
            id=product_id,
        )

        cart.remove(product)

        messages.success(
            request,
            "Product removed from cart.",
        )

        return redirect(
            "orders:cart",
        )


class CheckoutView(LoginRequiredMixin, View):

    def get(self, request):

        cart = Cart(request)

        if cart.is_empty():

            messages.warning(
                request,
                "Your cart is empty.",
            )

            return redirect(
                "orders:cart",
            )

        form = CheckoutForm(
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
            }
        )

        return render(
            request,
            "orders/checkout.html",
            {
                "form": form,
                "cart": cart,
            },
        )

    @transaction.atomic
    def post(self, request):

        cart = Cart(request)

        if cart.is_empty():

            messages.warning(
                request,
                "Your cart is empty.",
            )

            return redirect(
                "orders:cart",
            )

        form = CheckoutForm(request.POST)

        if not form.is_valid():

            return render(
                request,
                "orders/checkout.html",
                {
                    "form": form,
                    "cart": cart,
                },
            )

        for item in cart:

            product = item["product"]

            if not product.is_available:

                messages.error(
                    request,
                    f"{product.name} is currently unavailable.",
                )

                return redirect(
                    "orders:cart",
                )

            if item["quantity"] > product.inventory:

                messages.error(
                    request,
                    f"Only {product.inventory} units of {product.name} are available.",
                )

                return redirect(
                    "orders:cart",
                )

        order = Order.objects.create(

            user=request.user,

            first_name=form.cleaned_data["first_name"],

            last_name=form.cleaned_data["last_name"],

            email=form.cleaned_data["email"],

            phone_number=form.cleaned_data["phone_number"],

            address=form.cleaned_data["address"],

            description=form.cleaned_data["description"],

            coupon=cart.coupon,

            discount=cart.get_discount(),

        )

        for item in cart:

            product = item["product"]

            OrderItem.objects.create(

                order=order,

                product=product,

                quantity=item["quantity"],

                price=item["price"],

            )

            product.inventory -= item["quantity"]

            if product.inventory <= 0:

                product.inventory = 0

                product.is_available = False

            product.save()

        cart.clear()

        messages.success(
            request,
            "Your order has been created successfully.",
        )

        return redirect(
            "orders:success",
        )


class OrderSuccessView(LoginRequiredMixin, TemplateView):

    template_name = "orders/order_success.html"


class CouponApplyView(View):

    def post(self, request):

        form = CouponApplyForm(request.POST)

        if not form.is_valid():

            messages.error(
                request,
                "کد تخفیف معتبر نیست.",
            )

            return redirect("orders:cart")

        code = form.cleaned_data["code"]

        try:

            coupon = Coupon.objects.get(
                code__iexact=code,
                is_active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now(),
            )

            request.session["coupon_id"] = coupon.id

            messages.success(
                request,
                "کد تخفیف با موفقیت اعمال شد.",
            )

        except Coupon.DoesNotExist:

            request.session.pop(
                "coupon_id",
                None,
            )

            messages.error(
                request,
                "کد تخفیف نامعتبر یا منقضی شده است.",
            )

        return redirect("orders:cart")
