from decimal import Decimal
from datetime import time, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User
from menu.models import Category, Product
from orders.models import Coupon
from siteconfig.models import SiteSettings


class Command(BaseCommand):
    help = "Create demo data for CafeCore (categories, products, coupon, admin)."

    def handle(self, *args, **options):
        self.stdout.write("Seeding demo data...")

        # --- Site settings ---
        settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)
        if not settings_obj.site_name:
            settings_obj.site_name = "کافه کور"
            settings_obj.description = (
                "عشق در هواست… و بوی قهوه همه‌جا پیچیده."
            )
            settings_obj.save()
            self.stdout.write("  site settings OK")

        # --- Demo staff user ---
        admin_email = "admin@cafecore.local"
        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                email=admin_email,
                password="Admin123!",
                first_name="مدیر",
                last_name="دمو",
            )
            self.stdout.write(self.style.WARNING(
                f"  superuser created: {admin_email} / Admin123!"
            ))
        else:
            self.stdout.write("  superuser already exists")

        # --- Categories ---
        categories_data = [
            ("نوشیدنی گرم", "hot-drinks", "قهوه و نوشیدنی‌های گرم"),
            ("نوشیدنی سرد", "cold-drinks", "شیک و نوشیدنی‌های سرد"),
            ("غذای اصلی", "main-course", "غذاهای اصلی کافه"),
            ("دسر", "desserts", "شیرینی و دسر"),
        ]
        categories = {}
        for name, slug, desc in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "description": desc,
                    "is_active": True,
                },
            )
            categories[slug] = cat
            if created:
                self.stdout.write(f"  category: {name}")

        # --- Products ---
        products_data = [
            {
                "category": "hot-drinks",
                "name": "اسپرسو",
                "slug": "espresso",
                "description": "شات غلیظ اسپرسو ایتالیایی.",
                "price": 45000,
                "inventory": 50,
                "is_featured": True,
            },
            {
                "category": "hot-drinks",
                "name": "لاته",
                "slug": "latte",
                "description": "اسپرسو با شیر بخار‌داده و فوم نرم.",
                "price": 85000,
                "inventory": 40,
                "is_featured": True,
            },
            {
                "category": "hot-drinks",
                "name": "کاپوچینو",
                "slug": "cappuccino",
                "description": "ترکیب کلاسیک اسپرسو، شیر و فوم.",
                "price": 80000,
                "inventory": 40,
                "is_featured": False,
            },
            {
                "category": "cold-drinks",
                "name": "آیس لاته",
                "slug": "ice-latte",
                "description": "لاته خنک با یخ.",
                "price": 95000,
                "inventory": 30,
                "is_featured": True,
            },
            {
                "category": "cold-drinks",
                "name": "موهیتو",
                "slug": "mojito",
                "description": "نوشیدنی خنک نعناع و لیمو.",
                "price": 90000,
                "inventory": 25,
                "is_featured": False,
            },
            {
                "category": "main-course",
                "name": "پاستا آلفردو",
                "slug": "pasta-alfredo",
                "description": "پاستا با سس خامه‌ای قارچ.",
                "price": 280000,
                "inventory": 20,
                "is_featured": True,
            },
            {
                "category": "main-course",
                "name": "استیک مرغ",
                "slug": "chicken-steak",
                "description": "سینه مرغ گریل با سیب‌زمینی.",
                "price": 320000,
                "inventory": 15,
                "is_featured": True,
            },
            {
                "category": "main-course",
                "name": "سالاد سزار",
                "slug": "caesar-salad",
                "description": "کاهو، مرغ، نان برشته و سس سزار.",
                "price": 210000,
                "inventory": 20,
                "is_featured": False,
            },
            {
                "category": "desserts",
                "name": "چیزکیک",
                "slug": "cheesecake",
                "description": "چیزکیک کلاسیک با سس توت.",
                "price": 150000,
                "inventory": 15,
                "is_featured": True,
            },
            {
                "category": "desserts",
                "name": "براونی",
                "slug": "brownie",
                "description": "براونی شکلاتی گرم.",
                "price": 120000,
                "inventory": 20,
                "is_featured": False,
            },
            {
                "category": "desserts",
                "name": "تیرامیسو",
                "slug": "tiramisu",
                "description": "دسر ایتالیایی قهوه و ماسکارپونه.",
                "price": 160000,
                "inventory": 12,
                "is_featured": True,
            },
            {
                "category": "hot-drinks",
                "name": "چای ماسالا",
                "slug": "masala-chai",
                "description": "چای هندی با ادویه و شیر.",
                "price": 70000,
                "inventory": 35,
                "is_featured": False,
            },
        ]

        created_count = 0
        for item in products_data:
            cat = categories[item["category"]]
            _, created = Product.objects.get_or_create(
                slug=item["slug"],
                defaults={
                    "category": cat,
                    "name": item["name"],
                    "description": item["description"],
                    "price": Decimal(str(item["price"])),
                    "inventory": item["inventory"],
                    "is_available": True,
                    "is_featured": item["is_featured"],
                    "serving_start": time(10, 0),
                    "serving_end": time(23, 0),
                },
            )
            if created:
                created_count += 1

        self.stdout.write(f"  products created: {created_count}")

        # --- Coupon ---
        now = timezone.now()
        Coupon.objects.get_or_create(
            code="DEMO10",
            defaults={
                "discount": 10,
                "is_active": True,
                "valid_from": now - timedelta(days=1),
                "valid_to": now + timedelta(days=365),
            },
        )
        self.stdout.write("  coupon: DEMO10 (10%)")

        self.stdout.write(self.style.SUCCESS("Demo data is ready."))
