from django.contrib.auth import get_user_model
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
        harga = request.POST.get("harga")
        stock_gudang = request.POST.get("stock-gudang")
        user = User.objects.using('supplier_db').filter(id=request.user.id)
        supplier = Supplier.objects.filter(user=user)
        product = Product(supplier=supplier, product_name=product_name,
                          product_description=product_description, stock_gudang=stock_gudang, harga=harga)
        product.save(using='supplier_db')
    return render(request, 'home/create_product.html')


@login_required
def update_product(request):
    user = User.objects.using('supplier_db').filter(id=request.user.id)
    supplier = Supplier.objects.using('supplier_db').filter(user=user)
    product = Product.objects.using('supplier_db').filter(supplier=supplier)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        user = User.objects.using('supplier_db').filter(id=request.user.id)
        product = Product.objects.using(
            'supplier_db').filter(id=product_id, user=user)
        return redirect('supplier/dashboard')
    return render(request, 'home/update_product.html')


@login_required(login_url="/supplier/login")
def delete_product(request):
    product_id = request.POST.get('product_id')
    user = User.objects.using('supplier_db').filter(id=request.user.id)
    product = Product.objects.using(
        'supplier_db').filter(id=product_id, user=user)
    product.delete()
    return redirect("/supplier/dashboard")


@login_required(login_url="/supplier/login")
def show_dashboard(request):
    user = User.objects.get(id=request.user.id)
    print(user.id)

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


#  supplier = Supplier.objects.using('supplier_db').get(user_id=user.id)
#     products = Product.objects.using('supplier_db').filter(supplier=supplier)
#     paginator = Paginator(products, 10)  # 10 products per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
