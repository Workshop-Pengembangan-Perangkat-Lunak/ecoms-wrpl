from typing import Any
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    no_telp = models.CharField(max_length=32)
    location = models.CharField(max_length=200)
    no_rek = models.CharField(max_length=100)
    
    # def __str__(self):
    #     return f'{self.user.email} - {self.user.username}'


class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_description = models.CharField(max_length=100)
    product_category = models.CharField(max_length=100, default='lainnya')
    product_price = models.IntegerField()
    stock_gudang = models.IntegerField()
    product_image = models.ImageField(upload_to='product_images', default='default_product.jpg')
    supplier = models.CharField(max_length=100 , default='none')
    
    def __str__(self):
        return f'{self.product_name} - {self.product_price}'

class Transaction(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    buyer = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32, default='pending')
    
    def __str__(self):
        return f'{self.product_name} - {self.buyer}'
