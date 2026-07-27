from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import View

from menu.models import Product

from .forms import ReviewForm
from .models import Review


class ReviewCreateView(LoginRequiredMixin, View):

    def get(self, request, product_slug):

        product = get_object_or_404(
            Product,
            slug=product_slug,
            is_available=True,
        )

        form = ReviewForm()

        return render(
            request,
            "reviews/review_form.html",
            {
                "product": product,
                "form": form,
            },
        )

    def post(self, request, product_slug):

        product = get_object_or_404(
            Product,
            slug=product_slug,
            is_available=True,
        )

        if Review.objects.filter(
            user=request.user,
            product=product,
        ).exists():

            messages.warning(
                request,
                "You have already submitted a review for this product.",
            )

            return redirect(
                product.get_absolute_url(),
            )

        form = ReviewForm(request.POST)

        if not form.is_valid():

            return render(
                request,
                "reviews/review_form.html",
                {
                    "product": product,
                    "form": form,
                },
            )

        Review.objects.create(

            user=request.user,

            product=product,

            rating=form.cleaned_data["rating"],

            comment=form.cleaned_data["comment"],

        )

        messages.success(
            request,
            "Your review has been submitted successfully.",
        )

        return redirect(
            product.get_absolute_url(),
        )


class ProductReviewListView(TemplateView):

    template_name = "reviews/review_list.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        product = get_object_or_404(
            Product,
            slug=self.kwargs["product_slug"],
            is_available=True,
        )

        context["product"] = product

        context["reviews"] = Review.objects.filter(
            product=product,
            status=Review.Status.APPROVED,
        ).select_related(
            "user",
        )

        return context
