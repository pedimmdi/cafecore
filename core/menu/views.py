from django.db.models import Avg, Q
from django.views.generic import DetailView, ListView

from favorites.models import Favorite
from reviews.models import Review

from .models import Category, Product


class ProductListView(ListView):
    model = Product
    template_name = "menu/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        return (
            Product.objects
            .filter(is_available=True)
            .select_related("category")
            .order_by("name")
        )


class ProductDetailView(DetailView):
    model = Product
    template_name = "menu/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return (
            Product.objects
            .filter(is_available=True)
            .select_related("category")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        reviews = (
            Review.objects.filter(
                product=product,
                status=Review.Status.APPROVED,
            )
            .select_related("user")
            .order_by("-created_at")
        )
        context["reviews"] = reviews
        context["reviews_count"] = reviews.count()

        avg = reviews.aggregate(avg=Avg("rating"))["avg"]
        context["avg_rating"] = round(avg, 1) if avg else 0

        is_favorited = False
        user_has_reviewed = False
        if self.request.user.is_authenticated:
            is_favorited = Favorite.objects.filter(
                user=self.request.user,
                product=product,
            ).exists()
            user_has_reviewed = Review.objects.filter(
                user=self.request.user,
                product=product,
            ).exists()

        context["is_favorited"] = is_favorited
        context["user_has_reviewed"] = user_has_reviewed

        return context


class CategoryListView(ListView):
    model = Category
    template_name = "menu/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return (
            Category.objects
            .filter(is_active=True)
            .order_by("name")
        )


class CategoryDetailView(DetailView):
    model = Category
    template_name = "menu/category_detail.html"
    context_object_name = "category"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Category.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = (
            self.object.products.filter(is_available=True)
            .select_related("category")
            .order_by("name")
        )
        return context


class SearchView(ListView):
    model = Product
    template_name = "menu/search.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get("q")

        queryset = (
            Product.objects
            .filter(is_available=True)
            .select_related("category")
        )

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(ingredients__icontains=query)
            )

        return queryset.order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context
