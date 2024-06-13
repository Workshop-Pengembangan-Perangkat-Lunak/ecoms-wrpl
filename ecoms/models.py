from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


class Customer(models.Model):
    genders = [{'Male': 'male', 'Female': 'female'}]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=6, choices=genders, default='Male')
    picture = models.ImageField(upload_to='profile_pictures', default='default_picture.jpg')
    city = models.CharField(max_length=30, default='')
    subdistrict = models.CharField(max_length=30, default='')
    postal_code = models.CharField(max_length=30, default='')
    address = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.username


class Department(models.Model):
    dept_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.dept_name


class Product(models.Model):
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    buying_price = models.IntegerField()
    selling_price = models.IntegerField()
    description = models.CharField(max_length=100, default='')
    product_image = models.ImageField(upload_to='product_images')
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.product_name


class Transaction(models.Model):
    transaction_code = models.CharField(max_length=100)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    discount = models.IntegerField()
    total_price = models.IntegerField()
    payment_money = models.IntegerField()
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.transaction_code


class TransactionDetail(models.Model):
    transaction_code = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, default="")
    qty = models.IntegerField(default=1)
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.transaction_code)


class Cart(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.user_id)
