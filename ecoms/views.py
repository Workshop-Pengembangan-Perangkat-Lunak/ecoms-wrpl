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
    return render(request, 'register.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username, password)
        if user is not None:
            login(request, user)
            return redirect('/ecoms/shop')
    return render(request, 'login.html', {'form': form})


def create_product(request):
    pass


def show_products(request):
    department = Department.objects.all()
    products = Product.objects.all()
    if request.method == "POST":
        name_filter = request.POST.get('name_filter') or None
        dept_filter = request.POST.get('dept_filter') or None
        min_price = request.POST.get('min_price') or None
        max_price = request.POST.get('max_price') or None
        if name_filter:
            products = products.filter(
                product_name__icontains=f'{name_filter}')
        if dept_filter:
            products = products.filter(
                dept_id=department.filter(dept_name=dept_filter)).id
        if min_price and not max_price:
            products = products.filter(
                selling_price__range=[min_price, 99999999])
        elif max_price and not min_price:
            products = products.filter(selling_price__range=[0, max_price])
        elif max_price and min_price:
            products = products.filter(selling_price__range=[
                                       min_price, max_price])
        else:
            pass
    return render(request, 'index.html', {'products': products, 'departments': department})


def show_departments(request):
    depts = Department.objects.all()
    return render(request, 'dept.html', {'depts': depts})


def show_carts(request):
    carts = Cart.objects.all()
    return render(request, 'cart.html', {'carts': carts})


def show_shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})


def show_cart(request):
    carts = Cart.objects.all()
    subtotal = 0
    for cart in carts:
        subtotal += cart.product_id.selling_price * cart.qty
    context = {
        'carts': carts,
        'subtotal': subtotal
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


def show_user_trans(request):
    pass


def show_specific_products(request):
    products = Product.objects.filter(
        string__icontains=f"{request.POST.get('product_filter')}")
    return render(request, "products.html", {'products': products})


# @login_required(redirect_field_name='ecoms:login')
def add_to_cart(request):
    cart = CartForm(request.POST or None, initial={'qty': 1})
    if cart.is_valid():
        # cart.add_initial_prefix('qty', 1)
        cart.save()
        redirect('/ecoms/cart')
    return redirect('/ecoms/')


# @login_required()
def show_dashboard(request):
    transactions = Transaction.objects.all()
    return render(request, 'dashboard.html', {'transactions': transactions})
