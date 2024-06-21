from django.shortcuts import (
    render,
    redirect
)
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from supplier.models import Product as ProductSupplier, Supplier
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
from django.utils import timezone
from django.urls import reverse

def register_seller(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        location = request.POST.get('address')
        no_telp = request.POST.get('phone')
        no_rek = request.POST.get('no_rek')
        print(username, password, email, location, no_telp, no_rek)
        
        if not (username and password and email and location and no_telp and no_rek):
            messages.error(request, "Please fill out all fields.")
            return render(request, 'seller/home/register.html')
        try:
            user = User.objects.create_user(
                username=username, password=password, email=email)
            seller = Seller(
                user=user, no_telp=no_telp, location=location, no_rek=no_rek)
            
            if user.last_login is None:
                 user.last_login = timezone.now()
            user.save(using='seller_db')
            seller.save(using='seller_db')
            messages.success(request, "User registered succesfully")
            login(request, user)
            return redirect('/seller/dashboard')
        except Exception as e:
            print("error",e)
            messages.error(request, "Failed to register user.")
    return render(request, 'register_seller.html', {})


def login_seller(request):
    
    print("login seller")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            print("sukses auth")
            login(request, user)
            messages.success(request, f"Hi {username}")
            print("Redirecting to /seller/dashboard/") 
            return redirect(reverse('seller:dashboard'))
    return render(request, 'login_seller.html')

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
def get_product(request):
    user = User.objects.using('seller_db').get(id=request.user.id)
    seller = Seller.objects.using('seller_db').get(user=user)
    suppliers = Supplier.objects.using('supplier_db').all()
    products = None
    product = None
    
    if request.method == "POST":
        id_supplier = request.POST.get("supplier_id")
      
        supplier = Supplier.objects.using('supplier_db').filter(id=id_supplier).first()
       
        if id_supplier : 
            try:
                products = ProductSupplier.objects.using('supplier_db').filter(supplier=supplier)
            except ProductSupplier.DoesNotExist:
                products = None
        if request.POST.get("qty") is not None:
            qty = int(request.POST.get("qty"))
            product_id = request.POST.get("product_id")
            prod = ProductSupplier.objects.using('supplier_db').filter(id=product_id).first()
            if qty > prod.stock_gudang:
                messages.error(request, "Stock not enough")
                print("stock not enough")
                return render(request, 'get_product.html', {'suppliers': suppliers, 'products': products})
            else:
                if Product.objects.using('seller_db').filter(product_name=prod.product_name).exists():
                    product = Product.objects.using('seller_db').filter(product_name=prod.product_name).first()
                    product.stock_gudang += qty
                    product.save(using='seller_db')
                    prod.stock_gudang -= qty
                    prod.save(using='supplier_db')
                    messages.success(request, "Product added successfully")
                    return redirect('/seller/dashboard')
                else:
                    product_seller = Product(seller=seller, product_name=prod.product_name,
                                      product_description=prod.product_description, product_category=prod.product_category,  product_price=prod.product_price,stock_gudang=qty, supplier=prod.supplier.user.username)
                    prod.stock_gudang -= qty
                    product_seller.save(using='seller_db')
                    prod.save(using='supplier_db')
                    messages.success(request, "Product added successfully")
                    return redirect('/seller/dashboard')
    content = {
        'suppliers': suppliers,
        'products': products,
    }
    return render(request, 'get_product.html', content)

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

        product.product_name = request.POST.get("product_name")
        product.product_description = request.POST.get("product_description")
        product.product_category = request.POST.get("product_category")
        product.stock_gudang = request.POST.get("stock_gudang")
        product.product_price = request.POST.get("product_price")
        if request.FILES["product_image"] is not None:
            product.product_image = request.FILES["product_image"]
        product.save(using="seller_db")  # update product
        products = Product.objects.using(
            'seller_db').filter(seller = seller,)

        # paginator = Paginator(products, 10)  # 10 products per page
        # page_number = request.POST.get("page")
        # page_obj = paginator.get_page(page_number)
        # return render(request, 'tables_dashboard.html', {'page_obj': page_obj})
        return redirect("/seller/dashboard")
    return render(request, 'update_product_seller.html', {"product": product})

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
def delete_product(request, product_id):
    product = Product.objects.using('seller_db').get(id=product_id)
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
    user = User.objects.using('seller_db').get(id=request.user.id)
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
        return render(request, 'tables_dashboard.html', {'page_obj': page_obj, 'search': search})

    else:

        products = Product.objects.using(
            'seller_db').filter(seller = seller,)

        paginator = Paginator(products, 10)  # 10 products per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'tables_dashboard.html', {'page_obj': page_obj})


def logout_seller(request):
    logout(request)
    return redirect('/seller/login/')