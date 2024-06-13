from pyexpat.errors import messages
import uuid
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.csrf import csrf_exempt  # Add this line
from .models import Application, BankAccount, TopUpHistory, TransactionHistory

# handle login register for bank admin
def register_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            user = User.objects.create_user(
                username=username, password=password, email=email)
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
            return redirect('/bank/')
    return render(request, 'login.html')


from django.shortcuts import render, redirect
from .models import Application

# Handle user application
def show_applications(request, user_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        ktp = request.FILES.get('ktp')
        if name:  
                application = Application(name=name, ktp_photo=ktp, user_id=user_id)
                application.save()
                return redirect('bank:apply', user_id=user_id)
    application = Application.objects.all()
    return render(request, 'application.html', {'application':application})

def accept_application(request):
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        application_status = request.POST.get(application_status)
        application = Application.objects.get(id=application_id)
        application.status = application_status
        if application_status == 'S':
            bank_account = Application.bank_account
            bank_account.is_active = True
            bank_account.save()
        application.save()
        return redirect('bank')
import json

from midtransclient import Snap

#Handle user transaction with bank
# @require_POST
def create_transaction(request):
    # gross_amount = request.POST.get('gross_amount')
    user_id = request.POST.get('user_id')
    snap = Snap(
        is_production=False,
        server_key='SB-Mid-server-OUOnIHlPonXlJ3zt7M8mQkGX',  
        client_key='SB-Mid-client-zF1Nl-didCEzFYUM'
    )
    order_id = str(uuid.uuid4()) 

    param = {
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": 1000000,
        },
        "credit_card":{
            "secure" : True
        }
    }

    transaction = snap.create_transaction(param)
    print(transaction)
    TopUpHistory.objects.create(
        bank_account=BankAccount,
        transaction_type='P',
        amount=100000,
        order_id = order_id, 
        user_id = user_id
    )
    return redirect(transaction['redirect_url'])


def handle_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data['order_id']
        status_code = data['status_code']
        if status_code == '200':
            top_up = TopUpHistory.objects.get(order_id= order_id)
            user_id = top_up.user_id
            # Assuming 'other_database' is the alias for your other database
            user = User.objects.using('ecoms').get(id=user_id)
            user.balance += top_up.amount
            user.save(using='ecoms')
            
    return HttpResponse(status=200)

# handle transaction between users
from django.views.decorators.http import require_POST
from .models import TransactionHistory

def index_views(request):
    return render(request, 'home/tables.html')

@require_POST
def handle_transaction(request):
    # Get the source and destination account IDs from the POST data
    source_account_id = request.POST.get('source_account_id')
    destination_account_id = request.POST.get('destination_account_id')

    # Get the transaction amount from the POST data
    amount = request.POST.get('amount')

    # Get the source and destination accounts from the database
    source_account = get_object_or_404(BankAccount, user_id=source_account_id)
    destination_account = get_object_or_404(BankAccount, user_id=destination_account_id)

    # Check if the source account has enough balance for the transaction
    if source_account.balance < amount:
        return HttpResponse('Insufficient balance', status=400)

    # Deduct the amount from the source account's balance
    source_account.balance -= amount
    source_account.save()

    # Add the amount to the destination account's balance
    destination_account.balance += amount
    destination_account.save()

    # Create a new transaction history
    TransactionHistory.objects.create(
        source_account=source_account,
        destination_account=destination_account,
        transaction_type='P',
        amount=amount,
    )

    return HttpResponse('Transaction successful', status=200)