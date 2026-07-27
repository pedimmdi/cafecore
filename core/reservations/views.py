from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import View

from .forms import ReservationForm
from .models import Reservation


class ReservationCreateView(LoginRequiredMixin, View):

    def get(self, request):

        form = ReservationForm(
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
            }
        )

        return render(
            request,
            "reservations/reservation.html",
            {
                "form": form,
            },
        )

    def post(self, request):
        form = ReservationForm(request.POST)

        if not form.is_valid():

            return render(
                request,
                "reservations/reservation.html",
                {
                    "form": form,
                },
            )

        Reservation.objects.create(
            user=request.user,
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            email=form.cleaned_data["email"],
            phone_number=form.cleaned_data["phone_number"],
            reservation_date=form.cleaned_data["reservation_date"],
            reservation_time=form.cleaned_data["reservation_time"],
            number_of_guests=form.cleaned_data["number_of_guests"],
            description=form.cleaned_data["description"],
        )

        messages.success(request, "Your reservation has been submitted successfully.")
        return redirect("reservations:success")


class ReservationSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "reservations/reservation_success.html"
