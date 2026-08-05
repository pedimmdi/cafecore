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
            quantity = int(request.POST.get("quantity", 1))
        except (TypeError, ValueError):
            quantity = 1

        if quantity < 1:
            quantity = 1

        added = cart.add(product=product, quantity=quantity)

        if added:
            messages.success(request, "محصول به سبد اضافه شد.")
        else:
            messages.error(request, "امکان افزودن این محصول به سبد وجود ندارد.")

        return redirect("orders:cart")


class CartUpdateView(View):

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)

        try:
            quantity = int(request.POST.get("quantity", 1))
        except (TypeError, ValueError):
            quantity = 1

        cart.update(product=product, quantity=quantity)
        messages.success(request, "سبد خرید با موفقیت به‌روزرسانی شد.")
        return redirect("orders:cart")


class CartRemoveView(View):

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        messages.success(request, "محصول از سبد خرید حذف شد.")
        return redirect("orders:cart")


class CheckoutView(LoginRequiredMixin, View):

    def get(self, request):
        cart = Cart(request)
        if cart.is_empty():
            messages.warning(request, "سبد خرید شما خالی است.")
            return redirect("orders:cart")

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
            {"form": form, "cart": cart},
        )

    @transaction.atomic
    def post(self, request):
        cart = Cart(request)
        if cart.is_empty():
            messages.warning(request, "سبد خرید شما خالی است.")
            return redirect("orders:cart")

        form = CheckoutForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "orders/checkout.html",
                {"form": form, "cart": cart},
            )

        # کوپن ممکن است بین اعمال و چک‌اوت نامعتبر شده باشد
        coupon = cart.coupon
        if cart.coupon_id and coupon is None:
            messages.error(
                request,
                "کد تخفیف دیگر معتبر نیست و از سبد حذف شد.",
            )
            cart.clear_coupon()
            return redirect("orders:cart")

        for item in cart:
            product = item["product"]
            if not product.is_available:
                messages.error(
                    request,
                    f"{product.name} در حال حاضر در دسترس نیست.",
                )
                return redirect("orders:cart")
            if item["quantity"] > product.inventory:
                messages.warning(
                    request,
                    f"فقط {product.inventory} عدد از {product.name} موجود است.",
                )
                return redirect("orders:cart")

        order = Order.objects.create(
            user=request.user,
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            email=form.cleaned_data["email"],
            phone_number=form.cleaned_data["phone_number"],
            address=form.cleaned_data["address"],
            description=form.cleaned_data["description"],
            coupon=coupon,
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
        messages.success(request, "سفارش شما ثبت شد. لطفاً پرداخت را انجام دهید.")
        return redirect("payments:payment_request", order_id=order.id)


class OrderSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "orders/order_success.html"


class CouponApplyView(View):

    def post(self, request):
        form = CouponApplyForm(request.POST)
        if not form.is_valid():
            messages.error(request, "کد تخفیف معتبر نیست.")
            return redirect("orders:cart")

        code = form.cleaned_data["code"]
        user = request.user if request.user.is_authenticated else None

        try:
            coupon = Coupon.objects.get(code__iexact=code)
        except Coupon.DoesNotExist:
            request.session.pop("coupon_id", None)
            messages.error(request, "کد تخفیف نامعتبر یا منقضی شده است.")
            return redirect("orders:cart")

        if not coupon.is_usable(user=user):
            request.session.pop("coupon_id", None)
            if not coupon.is_within_date_range():
                messages.error(request, "کد تخفیف نامعتبر یا منقضی شده است.")
            elif coupon.max_uses and coupon.times_used() >= coupon.max_uses:
                messages.error(request, "سقف استفاده از این کد تخفیف پر شده است.")
            elif coupon.once_per_user and user:
                messages.error(request, "شما قبلاً از این کد تخفیف استفاده کرده‌اید.")
            else:
                messages.error(request, "امکان استفاده از این کد تخفیف وجود ندارد.")
            return redirect("orders:cart")

        request.session["coupon_id"] = coupon.id
        messages.success(request, "کد تخفیف با موفقیت اعمال شد.")
        return redirect("orders:cart")
