# Generated by Django 5.0.3 on 2024-06-24 09:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("product_name", models.CharField(max_length=100)),
                ("product_description", models.CharField(max_length=100)),
                ("product_category", models.CharField(max_length=100)),
                ("product_price", models.IntegerField()),
                ("stock_gudang", models.IntegerField()),
                (
                    "product_thumbnail",
                    models.ImageField(
                        blank=True, null=True, upload_to="product_images/"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="product_images/")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="supplier.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SellerBuyRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("request_stock", models.IntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("waiting", "waiting"),
                            ("accepted", "accepted"),
                            ("d", "declined"),
                        ],
                        default="waiting",
                        max_length=8,
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="supplier.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Supplier",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("no_telp", models.CharField(max_length=32)),
                ("location", models.CharField(max_length=200)),
                ("no_rek", models.CharField(max_length=100)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="supplier",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="supplier.supplier"
            ),
        ),
    ]
