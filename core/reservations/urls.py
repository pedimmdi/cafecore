from django.urls import path

from .views import ReservationCreateView
from .views import ReservationSuccessView


app_name = "reservations"


urlpatterns = [
    path("", ReservationCreateView.as_view(), name="reservation"),
    path("success/", ReservationSuccessView.as_view(), name="success"),
]
