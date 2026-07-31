from django.contrib import messages
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView,
    PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from .forms import RegisterForm, ProfileUpdateForm, LoginForm
from .models import User
from orders.models import Order
from reservations.models import Reservation
from reviews.models import Review
from payments.models import Payment


class RegisterView(View):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('accounts:login')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form':form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'حساب کاربری شما با موفقیت ایجاد شد')
            return redirect(self.success_url)
        context = {'form':form}
        return render(request, self.template_name, context)


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('pages:home')


class ProfileView(LoginRequiredMixin, View):
    template_name = "accounts/profile.html"

    def get(self, request, *args, **kwargs):
        from favorites.models import Favorite

        orders = (
            Order.objects.filter(user=request.user)
            .prefetch_related("items", "items__product")
            .order_by("-created_at")
        )
        reservations = (
            Reservation.objects.filter(user=request.user)
            .order_by("-created_at")
        )
        reviews = (
            Review.objects.filter(user=request.user)
            .select_related("product")
            .order_by("-created_at")
        )
        payments = (
            Payment.objects.filter(order__user=request.user)
            .select_related("order")
            .order_by("-created_at")
        )
        favorites = (
            Favorite.objects.filter(user=request.user)
            .select_related("product", "product__category")
            .order_by("-created_at")
        )

        context = {
            "user": request.user,
            "orders": orders,
            "reservations": reservations,
            "reviews": reviews,
            "payments": payments,
            "favorites": favorites,
        }
        return render(request, self.template_name, context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'پروفایل شما با موفقیت به‌روزرسانی شد')
        return super().form_valid(form)


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:password_change_done')


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/emails/password_reset_email.html'
    subject_template_name = 'accounts/emails/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
