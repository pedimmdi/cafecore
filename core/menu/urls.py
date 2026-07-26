from django.urls import path

from .views import (
    CategoryListView, ProductDetailView, ProductListView,
    CategoryDetailView, SearchView
)


app_name = "menu"

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("search/", SearchView.as_view(), name="search"),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
    path(
        "category/<slug:slug>/", CategoryDetailView.as_view(), name="category_detail"
    )
]
