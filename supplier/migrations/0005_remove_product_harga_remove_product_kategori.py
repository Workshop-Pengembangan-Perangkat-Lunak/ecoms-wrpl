# Generated by Django 5.0.3 on 2024-06-13 06:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("supplier", "0004_alter_product_product_description"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="harga",
        ),
        migrations.RemoveField(
            model_name="product",
            name="kategori",
        ),
    ]
