from django.shortcuts import (
    render,
    redirect
)
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import (
    csrf_protect,
    csrf_exempt
)
from django.core.paginator import Paginator


def register_seller(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        location = request.POST.get('address')
        no_telp = request.POST.get('phone')
        no_rek = request.POST.get('no-rek')
        try:
            user = User.objects.create_user(
                username=username, first_name=first_name, last_name=last_name, password=password, email=email)
            seller = Seller(
                user=user, no_telp=no_telp, address=location, no_rek=no_rek)
            user.save(using='seller_db')
            seller.save(using='seller_db')
            messages.success(request, "User registered succesfully")
            return redirect('/ecoms/login')
        except:
            messages.error(request, "Failed to register user.")
    return render(request, 'register.html', {})


def login_seller(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Hi {username}")
            return redirect('/seller/dashboard')
    return render(request, 'login.html')

@login_required(login_url="/seller/login")
def create_product(request):
    product_name = request.POST.get("nama-produk")
    product_description = request.POST.get("deskripsi-produk")
    stock_gudang = request.POST.get("stock-gudang")
    product_price = request.POST.get("harga-produk")
    user = User.objects.using('seller_db').filter(id=request.user.id)
    seller = Seller.objects.filter(user=user)
    product = Product(seller=seller, product_name=product_name,
                      product_description=product_description, stock_gudang=stock_gudang, product_price=product_price)
    product.save(using='seller_db')
    return render(request, 'create_product.html')

@login_required(login_url="/seller/login")
def create_transaction(request):
    product = request.POST.get("id-product")
    buyer = request.POST.get("buyer")
    quantity = request.POST.get("quantity")
    total_price = request.POST.get("total-price")
    transaction_date = request.POST.get("transaction-date")
    status = request.POST.get("status")
    user = User.objects.using('seller_db').filter(id=request.user.id)
    seller = Seller.objects.filter(user=user)
    product = Transaction(seller = seller, product=product, buyer = buyer, quantity=quantity, total_price=total_price, transaction_date=transaction_date, status=status)
    product.save(using='seller_db')
    return render(request, 'create_transaction.html')

@login_required(login_url="/seller/login")
def show_products(request):
    products = Product.objects.using('seller_db').all()
    return render(request, 'products.html', {'products': products})

@login_required(login_url="/seller/login")
def show_transactions(request):
    transactions = Transaction.objects.using('seller_db').all()
    return render(request, 'transactions.html', {'transactions': transactions})

@login_required(login_url="/seller/login")
def product_detail(request, product_id):
    product = Product.objects.using('seller_db').filter(id=product_id)
    return render(request, 'product_detail.html', {'product': product})
    
@login_required(login_url="/seller/login")
def transaction_detail(request, transaction_id):
    transaction = Transaction.objects.using('seller_db').filter(id=transaction_id)
    return render(request, 'transaction_detail.html', {'transaction': transaction})

@login_required(login_url="/seller/login")
def update_product(request, product_id):
    # try:
    user = User.objects.get(id=request.user.id)
    product = Product.objects.using('seller_db').get(id=product_id)
    seller = Seller.objects.using(
        'seller_db').get(user_id=user.id)
    if request.method == "POST":

        product.product_name = request.POST.get("nama-produk")
        product.product_description = request.POST.get("deskripsi-produk")
        product.stock_gudang = request.POST.get("stock-gudang")
        product.product_price = request.POST.get("harga-produk")
        product.save(using="seller_db")  # update product
        products = Product.objects.using(
            'seller_db').filter(seller = seller,)

        paginator = Paginator(products, 10)  # 10 products per page
        page_number = request.POST.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, 'home/tables.html', {'page_obj': page_obj})
    return render(request, 'home/update_product.html', {"product": product})

@login_required(login_url="/seller/login")
def update_transaction(request, transaction_id):
    # try:
    user = User.objects.get(id=request.user.id)
    transaction = Transaction.objects.using('seller_db').get(id=transaction_id)
    seller = Seller.objects.using(
        'seller_db').get(user_id=user.id)
    if request.method == "POST":

        transaction.product = request.POST.get("id-product")
        transaction.buyer = request.POST.get("buyer")
        transaction.quantity = request.POST.get("quantity")
        transaction.total_price = request.POST.get("total-price")
        transaction.transaction_date = request.POST.get("transaction-date")
        transaction.status = request.POST.get("status")
        transaction.save(using="seller_db")  # update product
        transactions = Product.objects.using(
            'seller_db').filter(seller = seller,)

        paginator = Paginator(transactions, 10)  # 10 products per page
        page_number = request.POST.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, 'home/tables.html', {'page_obj': page_obj})
    return render(request, 'home/update_transaction.html', {"transaction": transaction})

@login_required(login_url="/seller/login")
def delete_product(request):
    product_id = request.POST.get('product_id')
    user = User.objects.using('seller_db').filter(id=request.user.id)
    product = Product.objects.using(
        'seller_db').filter(id=product_id, user=user)
    product.delete()
    return redirect("/seller/dashboard")

@login_required(login_url="/seller/login")
def delete_transaction(request):
    transaction_id = request.POST.get('transaction_id')
    user = User.objects.using('seller_db').filter(id=request.user.id)
    transaction = Transaction.objects.using(
        'seller_db').filter(id=transaction_id, user=user)
    transaction.delete()
    return redirect("/seller/dashboard")


@login_required(login_url="/seller/login")
def show_dashboard(request):
    user = User.objects.get(id=request.user.id)
    print(user.id)

    seller = Seller.objects.using(
        'seller_db').get(user_id=user.id)

    if request.method == "POST":

        search = request.POST["search"]
        products = Product.objects.using('seller_db').filter(
            seller = seller, product_name__icontains=search)

        paginator = Paginator(products, 10)  # 10 products per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'home/tables.html', {'page_obj': page_obj, 'search': search})

    else:

        products = Product.objects.using(
            'seller_db').filter(seller = seller,)

        paginator = Paginator(products, 10)  # 10 products per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'home/tables.html', {'page_obj': page_obj})
