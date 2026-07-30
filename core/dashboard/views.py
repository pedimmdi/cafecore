from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.db.models import Sum
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
        # Orders
        # ======================

        context["paid_orders_count"] = (
            Order.objects.filter(
                status=Order.Status.PAID
            ).count()
        )

        context["pending_orders_count"] = (
            Order.objects.filter(
                status=Order.Status.PENDING
            ).count()
        )

        context["cancelled_orders_count"] = (
            Order.objects.filter(
                status=Order.Status.CANCELLED
            ).count()
        )

        # ======================
        # Latest Orders
        # ======================

        latest_orders = (
            Order.objects
            .select_related("user")
            .prefetch_related(
                "items",
                "items__product",
            )
            .order_by("-created_at")[:10]
        )

        context["latest_orders"] = latest_orders

        # ======================
        # Latest Reservations
        # ======================

        context["latest_reservations"] = (
            Reservation.objects
            .select_related("user")
            .order_by("-created_at")[:10]
        )

        # ======================
        # Latest Users
        # ======================

        context["latest_users"] = (
            User.objects
            .order_by("-date_joined")[:10]
        )

        # ======================
        # Latest Reviews
        # ======================

        context["latest_reviews"] = (
            Review.objects
            .select_related(
                "user",
                "product",
            )
            .order_by("-created_at")[:10]
        )

        # ======================
        # Low Inventory
        # ======================

        context["low_inventory_products"] = (
            Product.objects.filter(
                inventory__lte=10,
                is_available=True,
            ).order_by(
                "inventory"
            )[:10]
        )

        # ======================
        # Top Products
        # ======================

        context["top_products"] = (
            Product.objects.annotate(
                total_sales=Sum(
                    "order_items__quantity"
                )
            ).order_by(
                "-total_sales",
                "name",
            )[:10]
        )

        # ======================
        # Orders Chart
        # ======================

        context["orders_chart"] = (
            Order.objects
            .annotate(
                month=TruncMonth(
                    "created_at"
                )
            )
            .values(
                "month"
            )
            .annotate(
                total=Count(
                    "id"
                )
            )
            .order_by(
                "month"
            )
        )

        # ======================
        # Revenue
        # ======================

        total_revenue = 0

        for order in Order.objects.filter(
            status=Order.Status.PAID
        ).prefetch_related(
            "items"
        ):

            total_revenue += order.total_price

        context["total_revenue"] = total_revenue

        # ======================
        # Activity Timeline
        # ======================

        activities = []

        for order in latest_orders:

            activities.append({

                "type": "order",

                "title": f"Order #{order.id}",

                "created_at": order.created_at,

            })

        for reservation in context["latest_reservations"]:

            activities.append({

                "type": "reservation",

                "title": (
                    f"{reservation.first_name} "
                    f"{reservation.last_name}"
                ),

                "created_at": reservation.created_at,

            })

        for review in context["latest_reviews"]:

            activities.append({

                "type": "review",

                "title": review.product.name,

                "created_at": review.created_at,

            })

        activities.sort(
            key=lambda item: item["created_at"],
            reverse=True,
        )

        context["activities"] = activities[:20]

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

                "subtitle": (

                    f"{reservation.first_name} "

                    f"{reservation.last_name}"

                ),

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

                "time": user.date_joined,

            })

        activities.sort(

            key=lambda activity: activity["time"],

            reverse=True,

        )

        context["activities"] = activities[:20]

        return context
