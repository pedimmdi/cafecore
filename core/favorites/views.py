from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic import View

from menu.models import Product

from .models import Favorite


class FavoriteListView(LoginRequiredMixin, ListView):

    model = Favorite

    template_name = "favorites/favorites.html"

    context_object_name = "favorites"

    def get_queryset(self):

        return Favorite.objects.filter(
            user=self.request.user,
        ).select_related(
            "product",
        )


class FavoriteAddView(LoginRequiredMixin, View):

    def post(self, request, product_id):

        product = get_object_or_404(
            Product,
            id=product_id,
            is_available=True,
        )

        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            product=product,
        )

        if created:

            messages.success(
                request,
                "محصول به علاقه‌مندی‌ها اضافه شد.",
            )

        else:

            messages.info(
                request,
                "این محصول قبلاً در علاقه‌مندی‌های شما وجود دارد.",
            )

        return redirect(request.META.get("HTTP_REFERER", "menu:products"))


class FavoriteRemoveView(LoginRequiredMixin, View):

    def post(self, request, product_id):

        product = get_object_or_404(
            Product,
            id=product_id,
        )

        favorite = Favorite.objects.filter(
            user=request.user,
            product=product,
        )

        if favorite.exists():

            favorite.delete()

            messages.success(
                request,
                "محصول از علاقه‌مندی‌ها حذف شد.",
            )

        return redirect(request.META.get("HTTP_REFERER", "favorites:list"))
