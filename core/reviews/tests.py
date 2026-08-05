from django.db import IntegrityError
from django.test import TestCase

from accounts.models import User
from menu.models import Category, Product
from reviews.models import Review


class ReviewModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="reviewer@test.com",
            password="TestPass123!",
            first_name="کاربر",
            last_name="نظر",
        )
        self.category = Category.objects.create(name="دسر", slug="desserts-test")
        self.product = Product.objects.create(
            category=self.category,
            name="چیزکیک",
            slug="cheesecake-test",
            description="تست",
            price=100000,
            inventory=5,
            is_available=True,
        )

    def test_create_review_pending(self):
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            comment="عالی بود",
        )
        self.assertEqual(review.status, Review.Status.PENDING)

    def test_unique_review_per_user_product(self):
        Review.objects.create(
            user=self.user,
            product=self.product,
            rating=4,
            comment="خوب",
        )
        with self.assertRaises(IntegrityError):
            Review.objects.create(
                user=self.user,
                product=self.product,
                rating=3,
                comment="دوباره",
            )
