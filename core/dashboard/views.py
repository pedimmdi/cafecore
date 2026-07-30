from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from accounts.models import User
from menu.models import Product
from orders.models import Order
from reservations.models import Reservation
from reviews.models import Review


@method_decorator(staff_member_required, name="dispatch")
class DashboardView(TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ======================
        # Statistics
        # ======================
        context["users_count"] = User.objects.count()
        context["products_count"] = Product.objects.count()
        context["orders_count"] = Order.objects.count()
        context["reservations_count"] = Reservation.objects.count()
        context["reviews_count"] = Review.objects.count()

        # ======================
        # Orders by status
        # ======================
        context["paid_orders_count"] = Order.objects.filter(
            status=Order.Status.PAID
        ).count()
        context["pending_orders_count"] = Order.objects.filter(
            status=Order.Status.PENDING
        ).count()
        context["cancelled_orders_count"] = Order.objects.filter(
            status=Order.Status.CANCELLED
        ).count()

        # ======================
        # Latest data
        # ======================
        latest_orders = (
            Order.objects.select_related("user")
            .prefetch_related("items", "items__product")
            .order_by("-created_at")[:10]
        )
        context["latest_orders"] = latest_orders

        latest_reservations = (
            Reservation.objects.select_related("user")
            .order_by("-created_at")[:10]
        )
        context["latest_reservations"] = latest_reservations

        latest_users = User.objects.order_by("-created_at")[:10]
        context["latest_users"] = latest_users

        latest_reviews = (
            Review.objects.select_related("user", "product")
            .order_by("-created_at")[:10]
        )
        context["latest_reviews"] = latest_reviews

        # ======================
        # Low inventory
        # ======================
        context["low_inventory_products"] = (
            Product.objects.filter(inventory__lte=10, is_available=True)
            .order_by("inventory")[:10]
        )

        # ======================
        # Top products
        # ======================
        context["top_products"] = (
            Product.objects.annotate(
                total_sales=Sum("order_items__quantity")
            )
            .order_by("-total_sales", "name")[:10]
        )

        # ======================
        # Orders chart (monthly count)
        # ======================
        orders_by_month = (
            Order.objects.annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(total=Count("id"))
            .order_by("month")
        )

        orders_chart_labels = []
        orders_chart_values = []
        for item in orders_by_month:
            if item["month"]:
                orders_chart_labels.append(item["month"].strftime("%Y/%m"))
                orders_chart_values.append(item["total"])

        context["orders_chart_labels"] = orders_chart_labels
        context["orders_chart_values"] = orders_chart_values

        # ======================
        # Revenue chart (monthly revenue from paid orders)
        # ======================
        # Note: total_price is a property, so we calculate in Python
        revenue_by_month = {}
        paid_orders = (
            Order.objects.filter(status=Order.Status.PAID)
            .prefetch_related("items")
            .order_by("created_at")
        )

        total_revenue = 0
        for order in paid_orders:
            order_total = order.total_price
            # apply coupon discount if exists
            if order.discount:
                order_total = max(order_total - order.discount, 0)
            total_revenue += order_total

            month_key = order.created_at.strftime("%Y/%m")
            revenue_by_month[month_key] = (
                revenue_by_month.get(month_key, 0) + order_total
            )

        context["total_revenue"] = total_revenue
        context["revenue_chart_labels"] = list(revenue_by_month.keys())
        context["revenue_chart_values"] = list(revenue_by_month.values())

        # ======================
        # Activity timeline
        # ======================
        activities = []

        for order in latest_orders:
            activities.append({
                "icon": "bi-cart-check",
                "title": f"سفارش #{order.id} ثبت شد",
                "subtitle": f"{order.first_name} {order.last_name}",
                "time": order.created_at,
            })

        for reservation in latest_reservations:
            activities.append({
                "icon": "bi-calendar-check",
                "title": "رزرو جدید",
                "subtitle": f"{reservation.first_name} {reservation.last_name}",
                "time": reservation.created_at,
            })

        for review in latest_reviews:
            activities.append({
                "icon": "bi-chat-left-text",
                "title": "نظر جدید",
                "subtitle": review.product.name,
                "time": review.created_at,
            })

        for user in latest_users:
            activities.append({
                "icon": "bi-person-plus",
                "title": "کاربر جدید",
                "subtitle": user.email,
                "time": user.created_at,
            })

        activities.sort(key=lambda a: a["time"], reverse=True)
        context["activities"] = activities[:20]

        return context
