from django import forms
from django.utils import timezone
from django.db import models
import uuid

def upload_to(instance, filename):
    return 'ktp_photos/%s/%s' % (instance.name, filename)

class BankAccount(models.Model):
    user_id = models.IntegerField(max_length=20)
    name = models.CharField(max_length=200)
    bank_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    ktp_photo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.bank_number}'

class Application(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
    )

    name = models.CharField(max_length=200, default='')
    ktp_photo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    applied_at = models.DateTimeField(default=timezone.now)
    bank_account = models.OneToOneField(BankAccount, on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.IntegerField(max_length=20)

    def __str__(self):
        return f'{self.name} - {self.get_status_display()}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, 'bank_account'):
            BankAccount.objects.create(name=self.name, ktp_photo=self.ktp_photo)

class TopUpHistory(models.Model):
    TRANSACTION_TYPES = (
        ('D', 'Deposit'),
        ('W', 'Withdrawal'),
        ('P', 'Pending'),
        ('T', 'Transfer')
    )

    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    oder_id = models.CharField(max_length=30, default='')
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(default=timezone.now)
    user_id = models.IntegerField(max_length=20) 

    def __str__(self):
        return f'{self.bank_account.name} - {self.get_transaction_type_display()}'
    

class BankAdmin(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.username}'
    

class TransactionHistory(models.Model):
    TRANSACTION_TYPES = (
        ('D', 'Deposit'),
        ('W', 'Withdrawal'),
        ('P', 'Purchase'),
        ('T', 'Transfer')
    )

    source_account = models.ForeignKey('BankAccount', on_delete=models.CASCADE, related_name='outgoing_transactions')
    destination_account = models.ForeignKey('BankAccount', on_delete=models.CASCADE, related_name='incoming_transactions')
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    transaction_date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f'Transaction from account {self.source_account_id} to account {self.destination_account_id} - {self.get_transaction_type_display()}'
    