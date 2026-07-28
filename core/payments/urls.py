from django.urls import path

from .views import PaymentDetailView
from .views import PaymentFailedView
from .views import PaymentRequestView
from .views import PaymentVerifyView


app_name = "payments"


urlpatterns = [

    path("<int:order_id>/request/", PaymentRequestView.as_view(), name="payment_request"),
    path("<int:payment_id>/", PaymentDetailView.as_view(), name="payment_detail"),
    path("verify/", PaymentVerifyView.as_view(), name="payment_verify"),
    path("failed/", PaymentFailedView.as_view(), name="payment_failed"),
]
