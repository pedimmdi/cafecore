from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View

from .forms import ReservationForm
from .models import Reservation


class ReservationCreateView(LoginRequiredMixin, View):

    def get_initial(self, user):
        return {
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "email": user.email,
            "phone_number": user.phone_number or "",
        }

    def get(self, request):
        user = request.user
        form = ReservationForm(
            initial={
                "first_name": user.first_name or "",
                "last_name": user.last_name or "",
                "email": user.email,
                "phone_number": user.phone_number or "",
            }
        )
        return render(
            request,
            "reservations/reservation.html",
            {
                "form": form,
                "lock_first_name": bool(user.first_name),
                "lock_last_name": bool(user.last_name),
                "lock_phone": bool(user.phone_number),
            },
        )

    def post(self, request):
        form = ReservationForm(request.POST)
        user = request.user

        if not form.is_valid():
            return render(
                request,
                "reservations/reservation.html",
                {
                    "form": form,
                    "lock_first_name": bool(user.first_name),
                    "lock_last_name": bool(user.last_name),
                    "lock_phone": bool(user.phone_number),
                },
            )

        Reservation.objects.create(
            user=user,
            first_name=request.user.first_name or form.cleaned_data["first_name"],
            last_name=request.user.last_name or form.cleaned_data["last_name"],
            email=request.user.email,
            phone_number=request.user.phone_number or form.cleaned_data["phone_number"],
            reservation_date=form.cleaned_data["reservation_date"],
            reservation_time=form.cleaned_data["reservation_time"],
            number_of_guests=form.cleaned_data["number_of_guests"],
            description=form.cleaned_data.get("description") or "",
        )

        messages.success(request, "رزرو شما با موفقیت ثبت شد.")
        return redirect("reservations:success")


class ReservationSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "reservations/reservation_success.html"
