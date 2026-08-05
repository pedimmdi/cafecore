from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_alter_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="coupon",
            name="max_uses",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="حداکثر تعداد استفاده کلی. خالی = نامحدود",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="coupon",
            name="once_per_user",
            field=models.BooleanField(
                default=False,
                help_text="هر کاربر فقط یک‌بار بتواند از این کد استفاده کند",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="coupon",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orders",
                to="orders.coupon",
            ),
        ),
    ]
