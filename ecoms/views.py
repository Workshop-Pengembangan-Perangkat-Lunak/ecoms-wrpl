from .models import Customer, Cart, Transaction, TransactionDetail
from django.shortcuts import render, redirect
from .models import *
from seller.models import Product as SellerProduct
from delivery.models import Product as DeliveryProduct, Delivery
from django.db import connection
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from datetime import datetime
import uuid
# Create yoimpour views here.


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
        print("tes sebelum try", username, password )
        try:
            print(username," ", password, " ", email)
            user = User.objects.create_user(
                username=username, password=password, email=email)
            customer = Customer(
                user=user, first_name=first_name, last_name=last_name, phone=phone, address=address)
            customer.save()
            user.save()
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
    products = SellerProduct.objects.using('seller_db').all()
    for product in products:
        if not Department.objects.filter(dept_name=product.product_category).exists():
            dept = Department(dept_name=product.product_category)
            dept.save(using='default')
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
                product_category=Department.objects.get(dept_name=dept_filter))
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

def show_product_detail(request, pk):
    product = SellerProduct.objects.using('seller_db').get(id=pk)
    return render(request, 'product_detail.html', {'product': product})

def show_departments(request):
    depts = Department.objects.all()
    return render(request, 'dept.html', {'depts': depts})


def show_shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})


@login_required(login_url='login')
def show_cart(request):
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(user=user)
    carts = Cart.objects.filter(user_id=customer).all() or None
    subtotal = 0
    prod=[]
    if carts:
        for cart in carts:
            product = SellerProduct.objects.using('seller_db').get(id=cart.product_id)
            prod.append(product)
            subtotal += product.product_price * cart.qty
    
        cart_products = [{'cart': cart, 'product': product} for cart, product in zip(carts, prod)]
        context = {
            'carts': carts,
            'subtotal': subtotal,
            'customer': customer,
            'cart_products' : cart_products
        }
        return render(request, 'cart.html', context)
    context = {
            'subtotal': subtotal,
            'customer': customer,
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
    user_id = request.POST.get('user_id')
    prod_id = request.POST.get('product_id')
    # qty = request.POST.get('qty')
    user = User.objects.get(id=user_id)
    product = SellerProduct.objects.using('seller_db').get(id=prod_id)
    print("produknya",product.id)
    customer = Customer.objects.get(user=user)
    if Cart.objects.filter(user_id=customer, product_id=product.id).exists():
        cart = Cart.objects.get(user_id=customer, product_id=product.id)
        cart.qty += 1
    else:
        cart = Cart(user_id=customer, product_id=product.id)
    # cart = CartForm(request.POST or None, initial={'qty': 1})
    cart.save(using='default')
    return redirect('/ecoms')

def add_to_cart2(request, pk):
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(user=user)
    product = SellerProduct.objects.using('seller_db').get(id=pk)
    if Cart.objects.filter(user_id=customer, product_id=product.id).exists():
        cart = Cart.objects.get(user_id=customer, product_id=product.id)
        cart.qty += 1
    else:
        cart = Cart(user_id=customer, product_id=product.id)
        
    cart.save(using='default')
    return redirect('/ecoms/product_detail/'+str(pk))

def remove_from_cart(request, pk):
    cart = Cart.objects.get(id=pk)
    cart.delete()
    return redirect('/ecoms/cart')


@login_required(login_url='login')
def show_dashboard(request):
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(user=user)
    transactions = Transaction.objects.filter(user_id=customer).all()
    # transaction_details = TransactionDetail.objects.filter(transaction_code__in=transactions)
    
    # product_ids = transaction_details.values_list('product_id', flat=True)
    # print('product_ids', product_ids)
    # products = SellerProduct.objects.using('seller_db').filter(id__in=product_ids)
    # print('products', products)
    
    if not transactions.exists():
        context = {
        'transactions': transactions, 'customer': customer,
        }
        return render(request, 'dashboard.html', context)
    
    delivery = Delivery.objects.using('delivery_db').filter(user_id=customer.id)
    context = {
        'transactions': transactions, 'customer': customer, 'deliveries': delivery
    }
  
    return render(request, 'dashboard.html', context)

def update_profile(request,pk):
    user = User.objects.get(id=pk)
    customer = Customer.objects.get(user=user)
    if request.method == "POST":
        # print("firstName",request.POST.get('first_name'))
        #print(request.FILES['picture'])
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        sub_district = request.POST.get('subdistrict')
        postal_code = request.POST.get('postal_code')
    
        try:
            # customer = Customer( user=user,
            # first_name=first_name, last_name=last_name, phone=phone, address=address, city=city, sub_district=sub_district, postal_code=postal_code, picture=request.FILES['picture'], )
            customer.first_name = first_name
            customer.last_name = last_name
            customer.phone = phone
            customer.address = address
            customer.city = city
            customer.subdistrict = sub_district
            customer.postal_code = postal_code
            if 'picture' in request.FILES:
                customer.picture = request.FILES['picture']
            customer.save()
            return redirect('/ecoms/dashboard')
        except Exception as e:
            messages.error(request, "Failed to update.")
    return render(request, 'update_profile.html', {'customer': customer})

def logout_user(request):
    logout(request)
    messages.success(request, f"Have a nice day")
    return redirect('/ecoms/login')


# def checkout(request):
#     # quantity = request.POST.get('quantity')
#     # product_id = request.POST.get('product_id')
#     user = User(id=request.user.id)
#     customer = Customer(user=user)
#     carts = Cart.objects.filter(user_id=customer)
#     total_price = sum(
#         [cart.product_id.selling_price * cart.qty for cart in carts])
#     transaction = Transaction(
#         f"{request.id}-{carts.id}", request.id, 0, total_price, total_price, True)
#     transaction.save()
#     for cart in carts:
#         transaction_details = TransactionDetail(
#             transaction_code=transaction, product_id=cart.product_id, total=cart.product_id.selling_price*cart.qty)
#         transaction_details.save()
#         cart.delete()
#     return redirect('/ecoms/home')


@login_required
def checkout(request):
    if (request.method == 'POST'):
        qty = request.POST.get('qty')
        cart_id = request.POST.get('cart_id')
        if qty:
            cart = Cart.objects.get(id=cart_id)
            cart.qty = qty
            cart.save()
        return redirect('/ecoms/cart')
    customer = Customer.objects.get(user=request.user)
    carts = Cart.objects.filter(user_id=customer.id)
    products = SellerProduct.objects.using('seller_db').all()
    total_price = sum(
        [products.get(id=cart.product_id).product_price * cart.qty for cart in carts])
    transaction = Transaction(transaction_code=f"{request.user.id}{str(uuid.uuid4())}", user_id=customer, total_price=total_price, discount=0, payment_money=total_price)
    transaction.save()
    for cart in carts:
        transaction_details = TransactionDetail(
            transaction_code=transaction, product_id=cart.product_id, total=products.get(id=cart.product_id).product_price*cart.qty)
        transaction_details.save()
        product = SellerProduct.objects.using('seller_db').get(
            id=cart.product_id)
        
        print("customer",customer.id)
        delivery_product = DeliveryProduct( name = product.product_name, description = product.product_description)
        delivery_product.save(using='delivery_db')
        
        address = f"{customer.city} {customer.subdistrict} {customer.postal_code} {customer.address}"
        delivery = Delivery(user_id=customer.id,transaction_id=transaction.id, product=delivery_product, delivery_address=address, delivery_date=datetime.now(), status='P')
        delivery.save(using='delivery_db')
        
        product.stock_gudang = product.stock_gudang - cart.qty
        product.save(using='seller_db')
        cart.delete()  # Delete each cart after processing
    return redirect('/ecoms')

def checkout2(request,pk):
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(user=user)
    products = SellerProduct.objects.using('seller_db').all()
    if request.method == "POST":
        qty = request.POST.get('qty')
        if qty:
            cart = Cart.objects.get(user_id=customer, product_id=products.get(id=pk).id)
            cart.qty = qty
            cart.save()
        return redirect('/ecoms/cart')
    carts = Cart.objects.filter(user_id=customer.id)
    total_price = sum(
        [ products.get(id=cart.product_id).product_price * cart.qty for cart in carts])
    transaction = Transaction(transaction_code=f"{request.user.id}-{total_price}", user_id=customer, total_price=total_price, discount=0, payment_money=total_price)
    transaction.save()
    for cart in carts:
        transaction_details = TransactionDetail(
            transaction_code=transaction, product_id=cart.product_id, total=products.get(id=cart.product_id).product_price*cart.qty)
        transaction_details.save()
        product = SellerProduct.objects.using('seller_db').get(
            id=cart.product_id)
        product.stock_gudang = product.stock_gudang - cart.qty
        product.save(using='seller_db')
        cart.delete()  # Delete each cart after processing
    return redirect('/ecoms')

@login_required()
def show_user_id(request):
    return (request, 'test.html')
