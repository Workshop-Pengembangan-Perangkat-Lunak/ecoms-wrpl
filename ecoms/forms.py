from django.forms import ModelForm
from .models import *


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'gender', 'phone']


class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ['user_id', 'product_id', 'qty']
