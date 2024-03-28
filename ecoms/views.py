from django.shortcuts import render, redirect
from .models import *
from django.db import connection
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, csrf_exempt
# Create your views here.


def home(request):
    return render(request, 'index.html', {})


def register_user(request):
    '''
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/ecoms/login')
    '''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        try:
            user = User.objects.create_user(
                username=username, password=password)
            user.save()
            customer = Customer(user=user, first_name=first_name,
                                last_name=last_name, gender=gender, phone=phone, address=address)
            customer.save()
            messages.success(request, "User registered succesfully")
            return redirect('/ecoms/login')
        except:
            messages.error(request, "Failed to register user.")
    return render(request, 'register.html', {})


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Hi {username}")
            return redirect('/ecoms/')
    return render(request, 'login.html')


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
        sort_by = request.POST.get('sort_value') or None
        if name_filter:
            products = products.filter(
                product_name__icontains=f'{name_filter}').all()
        if dept_filter:
            products = products.filter(
                department_id=Department.objects.get(dept_name=dept_filter))
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
        if sort_by:
            products = products.order_by(sort_by)
    return render(request, 'index.html', {'products': products, 'departments': department})


def show_departments(request):
    depts = Department.objects.all()
    return render(request, 'dept.html', {'depts': depts})


@login_required(login_url='login')
def show_carts(request):
    carts = Cart.objects.all()
    return render(request, 'cart.html', {'carts': carts})


def show_shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})


@login_required(login_url='login')
def show_cart(request):
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(user=user)
    carts = Cart.objects.filter(user_id=customer).all() or None
    subtotal = 0
    if carts:
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


@login_required(login_url='login')
def add_to_cart(request):
    cart = CartForm(request.POST or None, initial={'qty': 1})
    if cart.is_valid():
        # cart.add_initial_prefix('qty', 1)
        cart.save()
        redirect('/ecoms/cart')
    return redirect('/ecoms/')


@login_required(login_url='login')
def show_dashboard(request):
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(user=user)
    transactions = Transaction.objects.filter(user_id=customer).all()
    return render(request, 'dashboard.html', {'transactions': transactions})


def logout_user(request):
    logout(request)
    messages.success(request, f"Have a nice day")
    return redirect('/ecoms/login')


def checkout(request):
    carts = Cart.objects.filter(user_id=request.id)
    total_price = sum(
        [cart.product_id.selling_price * cart.qty for cart in carts])
    transaction = Transaction(
        f"{request.id}-{carts.id}", request.id, 0, total_price, total_price, True)
    transaction.save()
    for cart in carts:
        transaction_details = TransactionDetail(
            transaction_code=transaction.id, product_id=cart.product_id, total=cart.product_id.selling_price*cart.qty)
        transaction_details.save()
    carts.delete()
    return redirect('/ecoms/home')


@login_required()
def show_user_id(request):
    return (request, 'test.html')
