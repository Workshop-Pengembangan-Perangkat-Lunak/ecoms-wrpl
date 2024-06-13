# Generated by Django 4.2.9 on 2024-06-13 06:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0007_bankadmin_application_bank_account_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactionhistory',
            name='bank_account',
        ),
        migrations.RemoveField(
            model_name='transactionhistory',
            name='bank_account_destination',
        ),
        migrations.AddField(
            model_name='application',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='transactionhistory',
            name='destination_account',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='incoming_transactions', to='bank.bankaccount'),
        ),
        migrations.AddField(
            model_name='transactionhistory',
            name='source_account',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_transactions', to='bank.bankaccount'),
        ),
        migrations.AlterField(
            model_name='transactionhistory',
            name='transaction_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='transactionhistory',
            name='transaction_type',
            field=models.CharField(choices=[('D', 'Deposit'), ('W', 'Withdrawal'), ('P', 'Purchase'), ('T', 'Transfer')], max_length=1),
        ),
        migrations.CreateModel(
            name='TopUpHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oder_id', models.CharField(default='', max_length=30)),
                ('transaction_type', models.CharField(choices=[('D', 'Deposit'), ('W', 'Withdrawal'), ('P', 'Pending'), ('T', 'Transfer')], max_length=1)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_id', models.IntegerField(default=0)),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank.bankaccount')),
            ],
        ),
    ]