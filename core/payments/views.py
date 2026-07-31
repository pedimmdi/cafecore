from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View

from orders.models import Order

from .models import Payment


class PaymentRequestView(LoginRequiredMixin, View):

    def get(self, request, order_id):
        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user,
        )

        if order.status == Order.Status.PAID:
            messages.info(request, "این سفارش قبلاً پرداخت شده است.")
            if hasattr(order, "payment"):
                return redirect(
                    "payments:payment_detail",
                    payment_id=order.payment.id,
                )
            return redirect("orders:success")

        if hasattr(order, "payment"):
            return redirect(
                "payments:payment_detail",
                payment_id=order.payment.id,
            )

        amount = order.total_price

        payment = Payment.objects.create(
            order=order,
            authority=f"PAY-{order.id}-{order.created_at.timestamp():.0f}",
            amount=amount,
        )

        messages.success(request, "درخواست پرداخت ایجاد شد.")
        return redirect(
            "payments:payment_detail",
            payment_id=payment.id,
        )


class PaymentDetailView(LoginRequiredMixin, TemplateView):
    template_name = "payments/payment_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["payment"] = get_object_or_404(
            Payment,
            id=self.kwargs["payment_id"],
            order__user=self.request.user,
        )
        return context


class PaymentVerifyView(LoginRequiredMixin, View):

    def get(self, request):
        authority = request.GET.get("Authority")
        payment = get_object_or_404(
            Payment,
            authority=authority,
            order__user=request.user,
        )

        payment.status = Payment.Status.SUCCESS
        payment.ref_id = f"REF-{payment.id}"
        payment.save()

        order = payment.order
        order.status = Order.Status.PAID
        order.save(update_fields=["status", "updated_at"])

        messages.success(request, "پرداخت با موفقیت انجام شد.")
        return redirect("payments:payment_detail", payment_id=payment.id)


class PaymentFailedView(LoginRequiredMixin, View):

    def get(self, request):
        authority = request.GET.get("Authority")
        payment = get_object_or_404(
            Payment,
            authority=authority,
            order__user=request.user,
        )

        payment.status = Payment.Status.FAILED
        payment.save()

        messages.error(request, "پرداخت ناموفق بود.")
        return redirect("payments:payment_detail", payment_id=payment.id)
