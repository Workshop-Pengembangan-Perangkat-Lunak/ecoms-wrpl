from django.contrib.auth import get_user_model, login
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

import logging

logger = logging.getLogger(__name__)


def authenticateSupplier(self, request, username=None, password=None, **kwargs):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.using('supplier_db').get(username=username)
        if user.check_password(password):
            return user
    except UserModel.DoesNotExist:
        return None


def registersupplier(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        location = request.POST.get('address')
        no_telp = request.POST.get('phone')
        no_rek = request.POST.get('no_rek')
        try:
            user = User.objects.create_user(
                username=username, password=password, email=email)
            supplier = Supplier(
                user=user, no_telp=no_telp, location=location, no_rek=no_rek)
            user.save(using='supplier_db')
            supplier.save(using='supplier_db')
            messages.success(request, "User registered succesfully")
            login(request, user)
            return redirect('/supplier/dashboard')
        except Exception as e:
            logger.error(f"Failed to register user: {e}")
            messages.error(request, "Failed to register user.")
    return render(request, 'home/register.html', {})


@csrf_exempt
def login_supplier(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print("user", user)
        if user is not None:
            login(request, user)
            messages.success(request, f"Hi {username}")
            return redirect('/supplier/dashboard')
    return render(request, 'home/login.html')


@login_required
def show_product(request):
    user = User.objects.using('supplier_db').filter(id=request.user.id)
    supplier = Supplier.objects.filter(user=user)
    return


@login_required(login_url="/supplier/login")
def create_product(request):
    if request.method == "POST":
        product_name = request.POST.get("nama-produk")
        product_description = request.POST.get("deskripsi-produk")
        product_category = request.POST.get("product_category")
        product_price = request.POST.get("product_price")
        stock_gudang = request.POST.get("stock-gudang")
        user = User.objects.using('supplier_db').filter(
            id=request.user.id).first()
        supplier = Supplier.objects.using(
            'supplier_db').filter(user=user).first()
        product = Product(supplier=supplier, product_name=product_name,
                          product_description=product_description, product_category=product_category, stock_gudang=stock_gudang, product_price=product_price)
        product.save(using='supplier_db')
        return redirect('supplier:dashboard')
    return render(request, 'home/create_product.html')


@login_required(login_url="/supplier/login")
def update_product(request, product_id):
    # try:
    user = User.objects.get(id=request.user.id)
    product = Product.objects.using('supplier_db').get(id=product_id)
    supplier = Supplier.objects.using(
        'supplier_db').get(user_id=user.id)
    if request.method == "POST":

        product.product_name = request.POST.get('product_name')
        product.product_description = request.POST.get('product_description')
        product.product_category = request.POST.get('product_category')
        product.stock_gudang = request.POST.get('stock_gudang')
        product.product_price = request.POST.get('product_price')
        product.save(using="supplier_db")  # update product
        products = Product.objects.using(
            'supplier_db').filter(supplier=supplier,)

        paginator = Paginator(products, 10)  # 10 products per page
        page_number = request.POST.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, 'home/tables.html', {'page_obj': page_obj})
    return render(request, 'home/update_product.html', {"product": product})


@login_required(login_url="/supplier/login")
def delete_product(request, product_id):
    # product_id = request.POST.get('product_id')
    product = Product.objects.using(
        'supplier_db').filter(id=product_id)
    product.delete()
    return redirect("/supplier/dashboard")


@login_required(login_url="/supplier/login")
def show_dashboard(request):
    user = User.objects.get(id=request.user.id)
    supplier = Supplier.objects.using(
        'supplier_db').get(user_id=user.id)

    if request.method == "POST":

        search = request.POST["search"]
        products = Product.objects.using('supplier_db').filter(
            supplier=supplier, product_name__icontains=search)

        paginator = Paginator(products, 10)  # 10 products per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'home/tables.html', {'page_obj': page_obj, 'search': search})
    else:
        products = Product.objects.using(
            'supplier_db').filter(supplier=supplier,)

        paginator = Paginator(products, 10)  # 10 products per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'home/tables.html', {'page_obj': page_obj})

def make_seller_request(request):
    product_id = request.POST.get('product_id')
    request_stock = request.POST.get('request_stock')
    product = Product.objects.get(id=product_id)
    seller_request = SellerBuyRequest(request_stock=request_stock, product=product)
    seller_request.save(using='supplier_db')
    return  

<<<<<<< HEAD
def accept_seller_request(request):
    product_id = request.POST.get('product_id')
    request_stock = request.POST.get('request_stock')
    product = Product.objects.using('supplier_db').filter(id=product_id)
    if int(request_stock) > int(product.stock_gudang):
        return JsonResponse(data={'message':'kebanyakan barangnya'})
    product.stock_gudang = product.stock_gudang - request_stock
    return redirect('seller:dashboard') 
=======
#  supplier = Supplier.objects.using('supplier_db').get(user_id=user.id)
#     products = Product.objects.using('supplier_db').filter(supplier=supplier)
#     paginator = Paginator(products, 10)  # 10 products per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)



def logout_supplier(request):
    logout(request)
    return redirect('/supplier/login')
>>>>>>> 3dcde21 (feature : get_prod,edit,update)
