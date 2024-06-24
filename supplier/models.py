from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    no_telp = models.CharField(max_length=32)
    location = models.CharField(max_length=200)
    no_rek = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_description = models.CharField(max_length=100)
    product_category = models.CharField(max_length=100)
    product_price = models.IntegerField()
    stock_gudang = models.IntegerField()
    product_thumbnail = models.ImageField(
        upload_to='product_images/', null=True, blank=True)


class SellerBuyRequest(models.Model):
    status_choices = [('waiting', 'waiting'),
                      ('accepted', 'accepted'), ('d', 'declined')]
    request_stock = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=8, choices=status_choices, default='waiting')

    def __str__(self):
        return f'{self.product_name} - {self.product_price}'


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
