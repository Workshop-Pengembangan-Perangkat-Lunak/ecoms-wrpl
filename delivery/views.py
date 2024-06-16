from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Product, Delivery
from .forms import DeliveryForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, csrf_exempt

def index(request):
    return render(request, 'deliveryindex.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def user_deliveries(request):
    deliveries = Delivery.objects.filter(user=request.user)
    return render(request, 'user_deliveries.html', {'deliveries': deliveries})

def add_delivery(request):
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('user_deliveries')
    else:
        form = DeliveryForm()
    return render(request, 'add_delivery.html', {'form': form})

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
        try:
            user = User.objects.create_user(
                username=username, password=password, email=email)
            user.save()
            messages.success(request, "User registered succesfully")
            return redirect('/delivery/login')
        except:
            messages.error(request, "Failed to register user.")
    return render(request, 'deliveryregister.html', {})


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Hi {username}")
            return redirect('/delivery')
    return render(request, 'deliverylogin.html')
