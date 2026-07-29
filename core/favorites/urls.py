from django.urls import path

from .views import (
    FavoriteAddView,
    FavoriteListView,
    FavoriteRemoveView,
)

app_name = "favorites"

urlpatterns = [

    path(
        "",
        FavoriteListView.as_view(),
        name="list",
    ),

    path(
        "add/<int:product_id>/",
        FavoriteAddView.as_view(),
        name="add",
    ),

    path(
        "remove/<int:product_id>/",
        FavoriteRemoveView.as_view(),
        name="remove",
    ),

]
