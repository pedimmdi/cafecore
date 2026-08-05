from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_order_coupon_order_discount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "در انتظار پرداخت"),
                    ("paid", "پرداخت شده"),
                    ("preparing", "در حال آماده‌سازی"),
                    ("ready", "آماده تحویل"),
                    ("delivered", "تحویل شده"),
                    ("cancelled", "لغو شده"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
    ]
