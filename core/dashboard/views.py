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
from django.utils import timezone

from accounts.models import User
from menu.models import Category, Product
from orders.models import Coupon, Order
from reservations.models import Reservation
from reviews.models import Review
from .forms import CategoryForm, CouponForm, InventoryUpdateForm, ProductForm


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
        if self.request.POST.get("image-clear"):
            if form.instance.image:
                form.instance.image.delete(save=False)
                form.instance.image = None
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
        if self.request.POST.get("image-clear"):
            if form.instance.image:
                form.instance.image.delete(save=False)
                form.instance.image = None
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


# ============================================================
# رزروها
# ============================================================

@method_decorator(staff_member_required, name="dispatch")
class ReservationListView(ListView):
    model = Reservation
    template_name = "dashboard/reservations/list.html"
    context_object_name = "reservations"
    paginate_by = 20

    def get_queryset(self):
        qs = Reservation.objects.select_related("user").order_by(
            "-reservation_date", "-reservation_time"
        )
        status = self.request.GET.get("status")
        q = self.request.GET.get("q", "").strip()

        if status in dict(Reservation.Status.choices):
            qs = qs.filter(status=status)
        if q:
            qs = qs.filter(
                models.Q(first_name__icontains=q)
                | models.Q(last_name__icontains=q)
                | models.Q(email__icontains=q)
                | models.Q(phone_number__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_status"] = self.request.GET.get("status", "")
        context["search_q"] = self.request.GET.get("q", "")
        context["status_choices"] = Reservation.Status.choices
        context["counts"] = {
            "all": Reservation.objects.count(),
            "pending": Reservation.objects.filter(
                status=Reservation.Status.PENDING
            ).count(),
            "confirmed": Reservation.objects.filter(
                status=Reservation.Status.CONFIRMED
            ).count(),
            "cancelled": Reservation.objects.filter(
                status=Reservation.Status.CANCELLED
            ).count(),
        }
        return context


@method_decorator(staff_member_required, name="dispatch")
class ReservationDetailView(DetailView):
    model = Reservation
    template_name = "dashboard/reservations/detail.html"
    context_object_name = "reservation"

    def get_queryset(self):
        return Reservation.objects.select_related("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Reservation.Status.choices
        return context


@method_decorator(staff_member_required, name="dispatch")
class ReservationStatusUpdateView(View):
    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        new_status = request.POST.get("status")
        valid = dict(Reservation.Status.choices)

        if new_status not in valid:
            messages.error(request, "وضعیت نامعتبر است.")
            return redirect("dashboard:reservation_detail", pk=pk)

        reservation.status = new_status
        reservation.save(update_fields=["status", "updated_at"])
        messages.success(
            request,
            f"وضعیت رزرو به «{valid[new_status]}» تغییر کرد.",
        )

        next_url = request.POST.get("next")
        if next_url:
            return redirect(next_url)
        return redirect("dashboard:reservation_detail", pk=pk)


# ============================================================
# نظرات
# ============================================================

@method_decorator(staff_member_required, name="dispatch")
class ReviewListView(ListView):
    model = Review
    template_name = "dashboard/reviews/list.html"
    context_object_name = "reviews"
    paginate_by = 20

    def get_queryset(self):
        qs = (
            Review.objects.select_related("user", "product")
            .order_by("-created_at")
        )
        status = self.request.GET.get("status")
        q = self.request.GET.get("q", "").strip()
        rating = self.request.GET.get("rating")

        if status in dict(Review.Status.choices):
            qs = qs.filter(status=status)
        if rating and rating.isdigit() and 1 <= int(rating) <= 5:
            qs = qs.filter(rating=int(rating))
        if q:
            qs = qs.filter(
                models.Q(comment__icontains=q)
                | models.Q(product__name__icontains=q)
                | models.Q(user__email__icontains=q)
                | models.Q(user__first_name__icontains=q)
                | models.Q(user__last_name__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_status"] = self.request.GET.get("status", "")
        context["current_rating"] = self.request.GET.get("rating", "")
        context["search_q"] = self.request.GET.get("q", "")
        context["status_choices"] = Review.Status.choices
        context["counts"] = {
            "all": Review.objects.count(),
            "pending": Review.objects.filter(status=Review.Status.PENDING).count(),
            "approved": Review.objects.filter(status=Review.Status.APPROVED).count(),
            "rejected": Review.objects.filter(status=Review.Status.REJECTED).count(),
        }
        return context


@method_decorator(staff_member_required, name="dispatch")
class ReviewDetailView(DetailView):
    model = Review
    template_name = "dashboard/reviews/detail.html"
    context_object_name = "review"

    def get_queryset(self):
        return Review.objects.select_related("user", "product")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Review.Status.choices
        return context


@method_decorator(staff_member_required, name="dispatch")
class ReviewStatusUpdateView(View):
    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        new_status = request.POST.get("status")
        valid = dict(Review.Status.choices)

        if new_status not in valid:
            messages.error(request, "وضعیت نامعتبر است.")
            return redirect("dashboard:review_detail", pk=pk)

        review.status = new_status
        review.save(update_fields=["status", "updated_at"])
        messages.success(
            request,
            f"وضعیت نظر به «{valid[new_status]}» تغییر کرد.",
        )

        next_url = request.POST.get("next")
        if next_url:
            return redirect(next_url)
        return redirect("dashboard:review_detail", pk=pk)


# ============================================================
# کوپن‌ها
# ============================================================

@method_decorator(staff_member_required, name="dispatch")
class CouponListView(ListView):
    model = Coupon
    template_name = "dashboard/coupons/list.html"
    context_object_name = "coupons"
    paginate_by = 20

    def get_queryset(self):
        qs = Coupon.objects.order_by("-created_at")
        status = self.request.GET.get("status")
        q = self.request.GET.get("q", "").strip()
        now = timezone.now()

        if status == "active":
            qs = qs.filter(is_active=True, valid_from__lte=now, valid_to__gte=now)
        elif status == "inactive":
            qs = qs.filter(is_active=False)
        elif status == "expired":
            qs = qs.filter(valid_to__lt=now)
        if q:
            qs = qs.filter(code__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["current_status"] = self.request.GET.get("status", "")
        context["search_q"] = self.request.GET.get("q", "")
        context["now"] = now
        context["counts"] = {
            "all": Coupon.objects.count(),
            "active": Coupon.objects.filter(
                is_active=True, valid_from__lte=now, valid_to__gte=now
            ).count(),
            "inactive": Coupon.objects.filter(is_active=False).count(),
            "expired": Coupon.objects.filter(valid_to__lt=now).count(),
        }
        return context


@method_decorator(staff_member_required, name="dispatch")
class CouponCreateView(CreateView):
    model = Coupon
    form_class = CouponForm
    template_name = "dashboard/coupons/form.html"
    success_url = reverse_lazy("dashboard:coupons")

    def form_valid(self, form):
        messages.success(self.request, "کوپن با موفقیت ایجاد شد.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "ایجاد کوپن"
        context["submit_label"] = "ثبت کوپن"
        return context


@method_decorator(staff_member_required, name="dispatch")
class CouponUpdateView(UpdateView):
    model = Coupon
    form_class = CouponForm
    template_name = "dashboard/coupons/form.html"
    success_url = reverse_lazy("dashboard:coupons")

    def form_valid(self, form):
        messages.success(self.request, "کوپن ویرایش شد.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "ویرایش کوپن"
        context["submit_label"] = "ذخیره تغییرات"
        return context


@method_decorator(staff_member_required, name="dispatch")
class CouponDeleteView(DeleteView):
    model = Coupon
    template_name = "dashboard/coupons/confirm_delete.html"
    success_url = reverse_lazy("dashboard:coupons")

    def form_valid(self, form):
        messages.success(self.request, "کوپن حذف شد.")
        return super().form_valid(form)


# ============================================================
# کاربران
# ============================================================

@method_decorator(staff_member_required, name="dispatch")
class UserListView(ListView):
    model = User
    template_name = "dashboard/users/list.html"
    context_object_name = "users"
    paginate_by = 20

    def get_queryset(self):
        qs = User.objects.order_by("-created_at")
        q = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status")

        if status == "active":
            qs = qs.filter(is_active=True)
        elif status == "inactive":
            qs = qs.filter(is_active=False)
        elif status == "staff":
            qs = qs.filter(is_staff=True)

        if q:
            qs = qs.filter(
                models.Q(email__icontains=q)
                | models.Q(first_name__icontains=q)
                | models.Q(last_name__icontains=q)
                | models.Q(phone_number__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_q"] = self.request.GET.get("q", "")
        context["current_status"] = self.request.GET.get("status", "")
        context["counts"] = {
            "all": User.objects.count(),
            "active": User.objects.filter(is_active=True).count(),
            "inactive": User.objects.filter(is_active=False).count(),
            "staff": User.objects.filter(is_staff=True).count(),
        }
        return context


@method_decorator(staff_member_required, name="dispatch")
class UserDetailView(DetailView):
    model = User
    template_name = "dashboard/users/detail.html"
    context_object_name = "profile_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context["user_orders"] = (
            Order.objects.filter(user=user)
            .prefetch_related("items")
            .order_by("-created_at")[:10]
        )
        context["user_reservations"] = (
            Reservation.objects.filter(user=user)
            .order_by("-created_at")[:10]
        )
        context["user_reviews"] = (
            Review.objects.filter(user=user)
            .select_related("product")
            .order_by("-created_at")[:10]
        )
        context["orders_count"] = Order.objects.filter(user=user).count()
        context["reservations_count"] = Reservation.objects.filter(user=user).count()
        context["reviews_count"] = Review.objects.filter(user=user).count()
        return context


@method_decorator(staff_member_required, name="dispatch")
class UserToggleActiveView(View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        # جلوگیری از غیرفعال کردن خودت
        if user.pk == request.user.pk:
            messages.error(request, "نمی‌توانید حساب خودتان را غیرفعال کنید.")
            return redirect("dashboard:user_detail", pk=pk)

        # جلوگیری از غیرفعال کردن سوپریوزر توسط غیرسوپریوزر
        if user.is_superuser and not request.user.is_superuser:
            messages.error(request, "دسترسی کافی برای این عملیات ندارید.")
            return redirect("dashboard:user_detail", pk=pk)

        user.is_active = not user.is_active
        user.save(update_fields=["is_active", "updated_at"])

        if user.is_active:
            messages.success(request, f"حساب «{user.email}» فعال شد.")
        else:
            messages.success(request, f"حساب «{user.email}» غیرفعال شد.")

        next_url = request.POST.get("next")
        if next_url:
            return redirect(next_url)
        return redirect("dashboard:user_detail", pk=pk)
