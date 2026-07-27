from django.urls import path

from .views import ProductReviewListView
from .views import ReviewCreateView


app_name = "reviews"


urlpatterns = [

    path(
        "<slug:product_slug>/",
        ProductReviewListView.as_view(),
        name="review_list",
    ),

    path(
        "<slug:product_slug>/create/",
        ReviewCreateView.as_view(),
        name="review_create",
    ),

]
