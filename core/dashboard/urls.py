from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="index"),

    # سفارش‌ها
    path("orders/", views.OrderListView.as_view(), name="orders"),
    path("orders/<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),
    path("orders/<int:pk>/status/", views.OrderStatusUpdateView.as_view(), name="order_status"),

    # محصولات
    path("products/", views.ProductListView.as_view(), name="products"),
    path("products/create/", views.ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/edit/", views.ProductUpdateView.as_view(), name="product_edit"),
    path("products/<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product_delete"),

    # دسته‌بندی‌ها
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path("categories/create/", views.CategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>/edit/", views.CategoryUpdateView.as_view(), name="category_edit"),
    path("categories/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="category_delete"),

    # موجودی
    path("inventory/", views.InventoryView.as_view(), name="inventory"),

    # رزروها
    path("reservations/", views.ReservationListView.as_view(), name="reservations"),
    path(
        "reservations/<int:pk>/",
        views.ReservationDetailView.as_view(),
        name="reservation_detail",
    ),
    path(
        "reservations/<int:pk>/status/",
        views.ReservationStatusUpdateView.as_view(),
        name="reservation_status",
    ),

    # نظرات
    path("reviews/", views.ReviewListView.as_view(), name="reviews"),
    path("reviews/<int:pk>/", views.ReviewDetailView.as_view(), name="review_detail"),
    path(
        "reviews/<int:pk>/status/",
        views.ReviewStatusUpdateView.as_view(),
        name="review_status",
    ),

    # کوپن‌ها
    path("coupons/", views.CouponListView.as_view(), name="coupons"),
    path("coupons/create/", views.CouponCreateView.as_view(), name="coupon_create"),
    path("coupons/<int:pk>/edit/", views.CouponUpdateView.as_view(), name="coupon_edit"),
    path("coupons/<int:pk>/delete/", views.CouponDeleteView.as_view(), name="coupon_delete"),

    # کاربران
    path("users/", views.UserListView.as_view(), name="users"),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path(
        "users/<int:pk>/toggle-active/",
        views.UserToggleActiveView.as_view(),
        name="user_toggle_active",
    ),
]
