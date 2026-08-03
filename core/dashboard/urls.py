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
]
