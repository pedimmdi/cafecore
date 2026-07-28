from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import View

from orders.models import Order

from .models import Payment


class PaymentRequestView(LoginRequiredMixin, View):

    def get(self, request, order_id):

        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user,
        )

        if hasattr(order, "payment"):

            return redirect(
                "payments:payment_detail",
                payment_id=order.payment.id,
            )

        amount = Decimal("0")

        for item in order.items.all():

            amount += item.price * item.quantity

        payment = Payment.objects.create(
            order=order,
            authority=f"PAY-{order.id}",
            amount=amount,
        )

        messages.success(
            request,
            "Payment request created successfully.",
        )

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

        payment.ref_id = "TEST-REF-ID"

        payment.save()

        messages.success(
            request,
            "Payment completed successfully.",
        )

        return redirect(
            "payments:payment_detail",
            payment_id=payment.id,
        )


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

        messages.error(
            request,
            "Payment failed.",
        )

        return redirect(
            "payments:payment_detail",
            payment_id=payment.id,
        )
