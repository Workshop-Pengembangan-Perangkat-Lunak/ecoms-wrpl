# Generated by Django 5.0.3 on 2024-06-23 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0003_remove_delivery_user_delivery_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='transaction_id',
            field=models.IntegerField(null=True),
        ),
    ]