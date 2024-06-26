
from datetime import timezone
from datetime import datetime

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
from django.db.models import Prefetch

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
            logger.debug("tess user create")

            user = User.objects.create_user(
                username=username, password=password, email=email)
            supplier = Supplier(
                user=user, no_telp=no_telp, location=location, no_rek=no_rek)
            logger.debug("tess user will saved")
            user.last_login = datetime.now()
            user.save(using='supplier_db')
            logger.debug("tess user saved")
            supplier.save(using='supplier_db')
            logger.debug("tess supplier saved")
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
        product_images = request.FILES.getlist('product_images')
        product = Product(supplier=supplier, product_name=product_name,
                          product_description=product_description, product_category=product_category, stock_gudang=stock_gudang, product_price=product_price,
                          product_thumbnail=product_images[0])
        product.save(using='supplier_db')

        for product_image in product_images:
            product_image = ProductImage(product=product, image=product_image)
            product_image.save(using='supplier_db')

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
        product_images = request.FILES.getlist('product_images')

        product.product_name = request.POST.get('product_name')
        product.product_description = request.POST.get('product_description')
        product.product_category = request.POST.get('product_category')
        product.stock_gudang = request.POST.get('stock_gudang')
        product.product_price = request.POST.get('product_price')
        product.product_thumbnail = product_images[0]

        product.save(using="supplier_db")  # update product

        for product_image in product_images:
            product_image = ProductImage(product=product, image=product_image)
            product_image.save(using='supplier_db')

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
    seller_request = SellerBuyRequest(
        request_stock=request_stock, product=product)
    seller_request.save(using='supplier_db')
    return


@login_required(login_url="/supplier/login")
def accept_seller_request(request):
    user = User.objects.using('supplier_db').get(id=request.user.id)
    supplier = Supplier.objects.using('supplier_db').get(user=user)
    product = Product.objects.using(
        'supplier_db').filter(supplier=supplier).all()
    seller_request = SellerBuyRequest.objects.using(
        'supplier_db').filter(product=product, status='waiting').all()

    if request.method == "POST":
        seller_request_id = request.POST.get('seller_request_id')
        request_stock = request.POST.get('request_stock')
        product_id = request.POST.get('product_id')
        product = Product.objects.using('supplier_db').filter(
            id=product_id).all()
        seller_request = SellerBuyRequest.objects.using(
            'supplier_db').filter(id=seller_request_id).all()
        if int(request_stock) > int(product.stock_gudang):
            return JsonResponse(data={'message': 'kebanyakan barangnya'})
        product.stock_gudang = product.stock_gudang - request_stock
        seller_request.status = 'accepted'
        return redirect('supplier:seller_request')
    return render(request, 'home/seller_request_tables.html', {'seller_requests': seller_request})
#  supplier = Supplier.objects.using('supplier_db').get(user_id=user.id)
#     products = Product.objects.using('supplier_db').filter(supplier=supplier)
#     paginator = Paginator(products, 10)  # 10 products per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)


def logout_supplier(request):
    logout(request)
    return redirect('/supplier/login')

