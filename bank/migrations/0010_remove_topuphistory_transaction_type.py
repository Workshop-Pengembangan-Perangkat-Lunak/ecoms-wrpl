# Generated by Django 3.2.6 on 2024-06-16 03:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0009_alter_transactionhistory_transaction_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topuphistory',
            name='transaction_type',
        ),
    ]
