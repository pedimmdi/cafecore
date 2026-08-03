from django.db import models
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Avg, Count, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import(
    DetailView, ListView, TemplateView, CreateView, DeleteView, UpdateView
)

from accounts.models import User
from menu.models import Category, Product
from orders.models import Coupon, Order
from reservations.models import Reservation
from reviews.models import Review
from .forms import CategoryForm, InventoryUpdateForm, ProductForm


@method_decorator(staff_member_required, name="dispatch")
class DashboardView(TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ---------- آمار کلی ----------
        context["users_count"] = User.objects.count()
        context["products_count"] = Product.objects.count()
        context["categories_count"] = Category.objects.count()
        context["orders_count"] = Order.objects.count()
        context["reservations_count"] = Reservation.objects.count()
        context["reviews_count"] = Review.objects.count()
        context["coupons_count"] = Coupon.objects.filter(is_active=True).count()

        context["paid_orders_count"] = Order.objects.filter(
            status=Order.Status.PAID
        ).count()
        context["pending_orders_count"] = Order.objects.filter(
            status=Order.Status.PENDING
        ).count()
        context["cancelled_orders_count"] = Order.objects.filter(
            status=Order.Status.CANCELLED
        ).count()

        context["pending_reservations_count"] = Reservation.objects.filter(
            status=Reservation.Status.PENDING
        ).count()
        context["confirmed_reservations_count"] = Reservation.objects.filter(
            status=Reservation.Status.CONFIRMED
        ).count()
        context["cancelled_reservations_count"] = Reservation.objects.filter(
            status=Reservation.Status.CANCELLED
        ).count()

        context["pending_reviews_count"] = Review.objects.filter(
            status=Review.Status.PENDING
        ).count()
        context["approved_reviews_count"] = Review.objects.filter(
            status=Review.Status.APPROVED
        ).count()

        context["low_inventory_count"] = Product.objects.filter(
            inventory__lte=10, is_available=True
        ).count()

        # ---------- درآمد کل ----------
        paid_orders = (
            Order.objects.filter(status=Order.Status.PAID)
            .prefetch_related("items")
            .order_by("created_at")
        )
        total_revenue = 0
        revenue_by_month = {}
        for order in paid_orders:
            order_total = order.total_price or 0
            total_revenue += order_total
            month_key = order.created_at.strftime("%Y/%m")
            revenue_by_month[month_key] = (
                revenue_by_month.get(month_key, 0) + float(order_total)
            )
        context["total_revenue"] = total_revenue
        context["revenue_chart_labels"] = list(revenue_by_month.keys())
        context["revenue_chart_values"] = list(revenue_by_month.values())

        # ---------- سفارش ماهانه ----------
        orders_by_month = (
            Order.objects.annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(total=Count("id"))
            .order_by("month")
        )
        context["orders_chart_labels"] = [
            item["month"].strftime("%Y/%m")
            for item in orders_by_month
            if item["month"]
        ]
        context["orders_chart_values"] = [
            item["total"] for item in orders_by_month if item["month"]
        ]

        # ---------- وضعیت سفارش (doughnut) ----------
        context["order_status_labels"] = ["در انتظار", "پرداخت‌شده", "لغوشده"]
        context["order_status_values"] = [
            context["pending_orders_count"],
            context["paid_orders_count"],
            context["cancelled_orders_count"],
        ]

        # ---------- وضعیت رزرو (doughnut) ----------
        context["reservation_status_labels"] = ["در انتظار", "تأییدشده", "لغوشده"]
        context["reservation_status_values"] = [
            context["pending_reservations_count"],
            context["confirmed_reservations_count"],
            context["cancelled_reservations_count"],
        ]

        # ---------- محصولات پرفروش (۵تایی) ----------
        top_products = (
            Product.objects.annotate(total_sales=Sum("order_items__quantity"))
            .order_by("-total_sales", "name")[:5]
        )
        context["top_products"] = top_products
        context["top_products_labels"] = [p.name for p in top_products]
        context["top_products_values"] = [
            int(p.total_sales or 0) for p in top_products
        ]

        # ---------- توزیع امتیاز نظرات ----------
        rating_dist = (
            Review.objects.filter(status=Review.Status.APPROVED)
            .values("rating")
            .annotate(total=Count("id"))
            .order_by("rating")
        )
        rating_map = {i: 0 for i in range(1, 6)}
        for item in rating_dist:
            rating_map[item["rating"]] = item["total"]
        context["rating_labels"] = [f"{i} ستاره" for i in range(1, 6)]
        context["rating_values"] = [rating_map[i] for i in range(1, 6)]

        # ---------- لیست‌های ۵تایی ----------
        context["latest_orders"] = (
            Order.objects.select_related("user")
            .prefetch_related("items", "items__product")
            .order_by("-created_at")[:5]
        )
        context["latest_reservations"] = (
            Reservation.objects.select_related("user")
            .order_by("-created_at")[:5]
        )
        context["latest_reviews"] = (
            Review.objects.select_related("user", "product")
            .order_by("-created_at")[:5]
        )
        context["latest_users"] = User.objects.order_by("-created_at")[:5]
        context["low_inventory_products"] = (
            Product.objects.filter(inventory__lte=10)
            .order_by("inventory")[:5]
        )

        # میانگین امتیاز
        avg_rating = (
            Review.objects.filter(status=Review.Status.APPROVED)
            .aggregate(avg=Avg("rating"))["avg"]
        )
        context["avg_rating"] = round(avg_rating, 1) if avg_rating else 0

        return context


@method_decorator(staff_member_required, name="dispatch")
class OrderListView(ListView):
    model = Order
    template_name = "dashboard/orders/list.html"
    context_object_name = "orders"
    paginate_by = 20

    def get_queryset(self):
        qs = (
            Order.objects.select_related("user", "coupon")
            .prefetch_related("items", "items__product")
            .order_by("-created_at")
        )
        status = self.request.GET.get("status")
        q = self.request.GET.get("q", "").strip()

        if status in dict(Order.Status.choices):
            qs = qs.filter(status=status)
        if q:
            qs = qs.filter(
                models.Q(first_name__icontains=q)
                | models.Q(last_name__icontains=q)
                | models.Q(email__icontains=q)
                | models.Q(phone_number__icontains=q)
                | models.Q(id__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_status"] = self.request.GET.get("status", "")
        context["search_q"] = self.request.GET.get("q", "")
        context["status_choices"] = Order.Status.choices
        context["counts"] = {
            "all": Order.objects.count(),
            "pending": Order.objects.filter(status=Order.Status.PENDING).count(),
            "paid": Order.objects.filter(status=Order.Status.PAID).count(),
            "cancelled": Order.objects.filter(status=Order.Status.CANCELLED).count(),
        }
        return context


@method_decorator(staff_member_required, name="dispatch")
class OrderDetailView(DetailView):
    model = Order
    template_name = "dashboard/orders/detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return (
            Order.objects.select_related("user", "coupon")
            .prefetch_related("items", "items__product")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Order.Status.choices
        try:
            context["payment"] = self.object.payment
        except Exception:
            context["payment"] = None
        return context


@method_decorator(staff_member_required, name="dispatch")
class OrderStatusUpdateView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get("status")

        valid = dict(Order.Status.choices)
        if new_status not in valid:
            messages.error(request, "وضعیت نامعتبر است.")
            return redirect("dashboard:order_detail", pk=pk)

        order.status = new_status
        order.save(update_fields=["status", "updated_at"])
        messages.success(
            request,
            f"وضعیت سفارش #{order.id} به «{valid[new_status]}» تغییر کرد.",
        )

        next_url = request.POST.get("next")
        if next_url:
            return redirect(next_url)
        return redirect("dashboard:order_detail", pk=pk)


# ============================================================
# محصولات
# ============================================================

@method_decorator(staff_member_required, name="dispatch")
class ProductListView(ListView):
    model = Product
    template_name = "dashboard/products/list.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        qs = Product.objects.select_related("category").order_by("-created_at")
        q = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("category")
        availability = self.request.GET.get("availability")

        if q:
            qs = qs.filter(
                models.Q(name__icontains=q) | models.Q(description__icontains=q)
            )
        if category:
            qs = qs.filter(category_id=category)
        if availability == "available":
            qs = qs.filter(is_available=True)
        elif availability == "unavailable":
            qs = qs.filter(is_available=False)
        elif availability == "low":
            qs = qs.filter(inventory__lte=10)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_q"] = self.request.GET.get("q", "")
        context["current_category"] = self.request.GET.get("category", "")
        context["current_availability"] = self.request.GET.get("availability", "")
        context["categories"] = Category.objects.filter(is_active=True)
        context["counts"] = {
            "all": Product.objects.count(),
            "available": Product.objects.filter(is_available=True).count(),
            "unavailable": Product.objects.filter(is_available=False).count(),
            "low": Product.objects.filter(inventory__lte=10).count(),
        }
        return context


@method_decorator(staff_member_required, name="dispatch")
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "dashboard/products/form.html"
    success_url = reverse_lazy("dashboard:products")

    def form_valid(self, form):
        messages.success(self.request, "محصول با موفقیت افزوده شد.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "افزودن محصول"
        context["submit_label"] = "ثبت محصول"
        return context


@method_decorator(staff_member_required, name="dispatch")
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "dashboard/products/form.html"
    success_url = reverse_lazy("dashboard:products")

    def form_valid(self, form):
        messages.success(self.request, "محصول با موفقیت ویرایش شد.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "ویرایش محصول"
        context["submit_label"] = "ذخیره تغییرات"
        return context


@method_decorator(staff_member_required, name="dispatch")
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "dashboard/products/confirm_delete.html"
    success_url = reverse_lazy("dashboard:products")

    def form_valid(self, form):
        messages.success(self.request, "محصول حذف شد.")
        return super().form_valid(form)


# ============================================================
# دسته‌بندی‌ها
# ============================================================

@method_decorator(staff_member_required, name="dispatch")
class CategoryListView(ListView):
    model = Category
    template_name = "dashboard/categories/list.html"
    context_object_name = "categories"
    paginate_by = 20

    def get_queryset(self):
        return Category.objects.annotate(
            products_count=Count("products")
        ).order_by("name")


@method_decorator(staff_member_required, name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "dashboard/categories/form.html"
    success_url = reverse_lazy("dashboard:categories")

    def form_valid(self, form):
        messages.success(self.request, "دسته‌بندی افزوده شد.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "افزودن دسته‌بندی"
        context["submit_label"] = "ثبت"
        return context


@method_decorator(staff_member_required, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "dashboard/categories/form.html"
    success_url = reverse_lazy("dashboard:categories")

    def form_valid(self, form):
        messages.success(self.request, "دسته‌بندی ویرایش شد.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "ویرایش دسته‌بندی"
        context["submit_label"] = "ذخیره"
        return context


@method_decorator(staff_member_required, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "dashboard/categories/confirm_delete.html"
    success_url = reverse_lazy("dashboard:categories")

    def form_valid(self, form):
        messages.success(self.request, "دسته‌بندی حذف شد.")
        return super().form_valid(form)


# ============================================================
# موجودی
# ============================================================

@method_decorator(staff_member_required, name="dispatch")
class InventoryView(ListView):
    model = Product
    template_name = "dashboard/inventory/list.html"
    context_object_name = "products"
    paginate_by = 30

    def get_queryset(self):
        qs = Product.objects.select_related("category").order_by("inventory", "name")
        filter_type = self.request.GET.get("filter", "low")
        if filter_type == "low":
            qs = qs.filter(inventory__lte=10)
        elif filter_type == "zero":
            qs = qs.filter(inventory=0)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_filter"] = self.request.GET.get("filter", "low")
        context["counts"] = {
            "all": Product.objects.count(),
            "low": Product.objects.filter(inventory__lte=10).count(),
            "zero": Product.objects.filter(inventory=0).count(),
        }
        return context

    def post(self, request, *args, **kwargs):
        """به‌روزرسانی سریع موجودی از جدول"""
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, pk=product_id)
        form = InventoryUpdateForm(request.POST, instance=product)
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.inventory <= 0:
                obj.inventory = 0
                obj.is_available = False
            form.save()
            messages.success(request, f"موجودی «{product.name}» به‌روز شد.")
        else:
            messages.error(request, "مقدار نامعتبر است.")
        return redirect(
            request.META.get("HTTP_REFERER", reverse_lazy("dashboard:inventory"))
        )
