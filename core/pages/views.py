from django.contrib import messages
from django.db.models import Q, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from menu.models import Category, Product
from orders.models import Order

from .forms import ContactForm
from .models import ContactMessage


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = (
            Category.objects.filter(is_active=True).order_by("name")[:8]
        )

        context["featured_products"] = (
            Product.objects.filter(
                is_available=True,
                is_featured=True,
            )
            .select_related("category")
            .order_by("name")[:8]
        )

        context["popular_products"] = (
            Product.objects.filter(is_available=True)
            .select_related("category")
            .annotate(
                total_sales=Coalesce(
                    Sum(
                        "order_items__quantity",
                        filter=Q(
                            order_items__order__status__in=Order.REVENUE_STATUSES
                        ),
                    ),
                    Value(0),
                )
            )
            .order_by("-total_sales", "name")[:12]
        )

        context["products_count"] = Product.objects.filter(
            is_available=True
        ).count()

        return context


class AboutView(TemplateView):
    template_name = "pages/about.html"


class ContactView(View):
    template_name = "pages/contact.html"
    form_class = ContactForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(
            request,
            self.template_name,
            {"form": form},
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                subject=form.cleaned_data["subject"],
                message=form.cleaned_data["message"],
            )
            messages.success(
                request,
                "پیام شما با موفقیت ارسال شد.",
            )
            return redirect("pages:contact")

        return render(
            request,
            self.template_name,
            {"form": form},
        )
