from django.urls import path

from .views import (
    RegisterView, CustomLoginView, CustomLogoutView,
    ProfileView, ProfileUpdateView, CustomPasswordChangeView,
    CustomPasswordChangeDoneView, CustomPasswordResetView,
    CustomPasswordResetDoneView, CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

app_name = "accounts"

urlpatterns = [
    path(
        "register/", RegisterView.as_view(), name="register",
    ),
    path(
        "login/", CustomLoginView.as_view(), name="login",
    ),
    path(
        "logout/", CustomLogoutView.as_view(), name="logout",
    ),
    path(
        "profile/", ProfileView.as_view(), name="profile",
    ),
    path(
        "profile/edit/", ProfileUpdateView.as_view(),
        name="profile_edit",
    ),
    path(
        "password/change/", CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password/change/done/", CustomPasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "password/reset/", CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password/reset/done/", CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password/reset/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password/reset/complete/", CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
