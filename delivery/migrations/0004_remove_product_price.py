# Generated by Django 5.0.3 on 2024-06-16 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
    ]
