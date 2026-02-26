# Add landmark field to Order

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0014_report_order_address_order_created_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="landmark",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
