from django.shortcuts import (
    render,
    redirect
)
from django.http import JsonResponse
from django.contrib import messages


def register_supllier(request):
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
                username=username, password=password, email=email)
            customer = Customer(
                user=user, first_name=first_name, last_name=last_name, phone=phone, address=address)
            customer.save()
            user.save()
            customer = Customer(user=user, first_name=first_name,
                                last_name=last_name, gender=gender, phone=phone, address=address)
            customer.save()
            messages.success(request, "User registered succesfully")
            return redirect('/ecoms/login')
        except:
            messages.error(request, "Failed to register user.")
    return render(request, 'register.html', {})


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Hi {username}")
            return redirect('/ecoms/')
    return ""


def show_product():
    return


def create_product():
    return


def update_product():
    return


def delete_product():
    return
