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


def register_supllier(request):
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
            supplier = Supplier(
                user=user, no_telp=no_telp, address=location, no_rek=no_rek)
            user.save(using='supplier_db')
            supplier.save(using='supplier_db')
            messages.success(request, "User registered succesfully")
            return redirect('/ecoms/login')
        except:
            messages.error(request, "Failed to register user.")
    return render(request, 'register.html', {})


def login_supplier(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Hi {username}")
            return redirect('/supplier/dashboard')
    return ""


def show_product(request):
    return


@login_required
def create_product(request):
    product_name = request.POST.get("nama-produk")
    product_description = request.POST.get("deskripsi-produk")
    stock_gudang = request.POST.get("stock-gudang")
    user = User.objects.using('supplier_db').filter(id=request.user.id)
    supplier = Supplier.objects.filter(user=user)
    product = Product(supplier=supplier, product_name=product_name,
                      product_description=product_description, stock_gudang=stock_gudang)
    product.save(using='supplier_db')
    return


def update_product(request):
    return


@login_required
def delete_product(request):
    product_id = request.POST.get('product_id')
    user = User.objects.using('supplier_db').filter(id=request.user.id)
    product = Product.objects.using(
        'supplier_db').filter(id=product_id, user=user)
    product.delete()
    return redirect("/supplier/dashboard")


@login_required
def show_dashboard(request):
    return
