from django.forms import ModelForm
from django import forms
from .models import *


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'gender',
            'phone',
            'address'
        ]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password'
        ]


class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = [
            'user_id',
            'product_id',
            'qty'
        ]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
