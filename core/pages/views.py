from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from .forms import ContactForm
from .models import ContactMessage


class HomeView(TemplateView):
    template_name = "pages/home.html"


class AboutView(TemplateView):
    template_name = "pages/about.html"


class ContactView(View):

    template_name = "pages/contact.html"

    form_class = ContactForm

    def get(self, request, *args, **kwargs):

        form = self.form_class()

        context = {
            "form": form,
        }

        return render(
            request,
            self.template_name,
            context,
        )

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            ContactMessage.objects.create(

                name=form.cleaned_data["name"],

                email=form.cleaned_data["email"],

                subject=form.cleaned_data["subject"],

                message=form.cleaned_data["message"],

            )

            messages.success(
                request,
                "پیام شما با موفقیت ارسال شد.",
            )

            return redirect("pages:contact")

        context = {
            "form": form,
        }

        return render(
            request,
            self.template_name,
            context,
        )
