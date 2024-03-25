from django.shortcuts import render, redirect
from .models import *
from django.db import connection
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, 'index.html', {})


def register_user(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('food:login')
    return render(request, '', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username, password)
        if user is not None:
            login(request, user)
            return redirect('ecoms:shop')
    else:
        form = LoginForm()
    return render(request, '', {'form': form})


def create_product(request):
    pass


def show_products(request):
    if request.method == "POST":
        filter = request.POST.get('filter')
        products = Product.objects.filter(product_name__icontains=f'{filter}')
        return render(request, 'index.html', {'products': products})
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def show_departments(request):
    depts = Department.objects.all()
    return render(request, 'dept.html', {'depts': depts})


def show_carts(request):
    carts = Cart.objects.all()
    return render(request, 'cart.html', {'carts': carts})


def show_shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})


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


def show_user_trans(request):
    pass


def show_specific_products(request):
    products = Product.objects.filter(
        string__icontains=f"{request.POST.get('product_filter')}")
    return render(request, "products.html", {'products': products})


@login_required(redirect_field_name='ecoms:login')
def add_to_cart(request):
    cart = CartForm(request.POST or None)
    if cart.is_valid():
        cart.save()
        redirect('ecoms:carts')
    return redirect('ecoms:products')


@login_required()
def show_dashboard(request):
    transactions = Transaction.objects.all(pk=request.user.id)
    return render(request, 'dashboard.html', {'transactions': transactions})
