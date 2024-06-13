from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    no_telp = models.CharField(max_length=32)
    location = models.CharField(max_length=200)
    no_rek = models.CharField(max_length=100)


class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_description = models.IntegerField()
    stock_gudang = models.IntegerField()
