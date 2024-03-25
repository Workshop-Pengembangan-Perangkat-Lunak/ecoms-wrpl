from django.shortcuts import render, redirect
from .models import *
from django.db import connection
from .forms import CartForm
# Create your views here.


def home(request):
    return render(request, 'index.html', {})


def create_product(request):
    pass


def show_products(request):
    if request.method == "POST":
        filter = request.POST.get('filter')
        products = Product.objects.filter(product_name__icontains=f'{filter}')
        return render(request, 'products.html', {'products': products})
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


def show_departments(request):
    depts = Department.objects.all()
    return render(request, 'dept.html', {'depts': depts})


def show_carts(request):
    carts = Cart.objects.all()
    return render(request, 'carts.html', {'carts': carts})

def show_shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})

def show_cart(request):
    carts = Cart.objects.all()
    subtotal = 0
    for cart in carts:
        subtotal += cart.product_id.selling_price * cart.qty
    context = {
        'carts' : carts,
        'subtotal' : subtotal
    }
    return render(request, 'cart.html', context)

def show_shop_detail(request, id):
    products = Product.objects.filter(id=id)
    return render(request, 'shop_detail.html', {'products': products})



def show_transactions(request):
    transactions = Transaction.objects.all()
    return render(request, 'trans.html', {'transactions': transactions})


def show_users(request):
    users = Customer.objects.all()
    return render(request, 'users.html', {'users': users})


def show_specific_user(request):
    pass


def show_user_cart(request):
    pass


def show_user_trans(request):
    pass


# def show_specific_products(request):
#     products = Product.objects.filter(
#         string__icontains=f"{request.POST.get("product_filter")}")
#     return render(request, "products.html", {'products': products})

def show_specific_products(request):
    products = Product.objects.filter(
        string__icontains=f"{request.POST.get('product_filter')}")
    return render(request, "products.html", {'products': products})

def add_to_cart(request):
    cart = CartForm(request.POST or None)
    if cart.is_valid():
        cart.save()
        redirect('ecoms:carts')
    return redirect('ecoms:products')
