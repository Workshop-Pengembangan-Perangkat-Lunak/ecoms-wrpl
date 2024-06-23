from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Delivery(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('I', 'In Progress'),
        ('D', 'Delivered'),
    ]
    # user = models.ForeignKey(User, on_delete=models.CASCADE,default='')
    user_id = models.IntegerField(null=True)
    transaction_id = models.IntegerField(null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=255)
    delivery_date = models.DateTimeField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    def __str__(self):
        return f"{self.product.name} - {self.status}"
