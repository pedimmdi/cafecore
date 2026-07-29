from django.urls import path

from .views import (
    CartAddView,
    CartDetailView,
    CartRemoveView,
    CartUpdateView,
    CheckoutView,
    OrderSuccessView,
    CouponApplyView,
)

app_name = "orders"

urlpatterns = [
    path("cart/", CartDetailView.as_view(), name="cart"),
    path("cart/add/<int:product_id>/", CartAddView.as_view(), name="cart_add"),
    path(
        "cart/remove/<int:product_id>/", CartRemoveView.as_view(), name="cart_remove"
    ),
    path(
        "cart/update/<int:product_id>/", CartUpdateView.as_view(), name="cart_update"
    ),
    path("coupon/apply/", CouponApplyView.as_view(), name="coupon_apply"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("success/", OrderSuccessView.as_view(), name="success"),
]
