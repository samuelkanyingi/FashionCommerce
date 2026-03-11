# Generated manually to fix out-of-sync database

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='checkout_request_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
