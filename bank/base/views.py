from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.
from django.contrib.auth.forms import UserCreationForm

from base.filters import TransactionFilter
from .forms import CreateUserForm, DepositForm, WithdrawForm, TransferForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction, User

def index(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:
        return render(request, "index.html")

def register(request):
    
    if request.user.is_authenticated:
        return redirect("dashboard") 
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()

                user = form.cleaned_data.get("username")
                messages.success(request, user + "'s Account Created Successfully")

                return redirect("login")

        context = {"form": form}
        return render(request, "register.html", context)

def login_page(request):
    
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.info(request, "Username or Password Incorrect")

        context = {}
        return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    return redirect("index")
    

    context = {}
    return render(request, "login.html", context)

@login_required(login_url="index")
def dashboard(request):
    # account = Account.objects.filter(user=request.user)
    account = get_object_or_404(Account, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-transaction_date')[:3]
    

    context = {'account':account, 'transactions':transactions}
    return render(request, "dashboard.html", context)

@login_required(login_url="index")
def deposit(request):
    form = DepositForm()
    
    try:
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        messages.error(request, "Your account does not exist.")
        return redirect("dashboard")
    
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            
            Transaction.objects.create(
                account=account,
                type='deposit',
                amount=amount
            )
            
            messages.success(request, 'Deposit successful.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Something Went Wrong.')
    else:
        form = DepositForm()
    
    
    context = {'form': form}
    return render(request, 'deposit.html', context)

@login_required(login_url="index")
def withdraw(request):
    form = WithdrawForm()
    try:
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        messages.error(request, "Your account does not exist.")
        return redirect("dashboard")
    
    if request.method == "POST":
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            if account.balance >= amount:
                account.balance -= amount
                account.save()

                Transaction.objects.create(
                    account=account,
                    type = "withdraw",
                    amount=amount
                )
                messages.success(request, "Withdrawl Successful!")
                return redirect("dashboard")
            else:
                messages.error(request, "Oops! Insufficient Balance")
        else:
            messages.error(request, 'Something Went Wrong.')
    else:
        form = WithdrawForm()

    context = {"form":form}        
    return render(request, "withdraw.html", context)

@login_required(login_url="index")
def transfer(request):
    try:
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        messages.error(request, "Your account does not exist.")
        return redirect("dashboard")
    
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            destination_account_number = form.cleaned_data["destination_account_number"]
            try:
                destination_account = Account.objects.get(account_number=destination_account_number)
                if account.balance >= amount:
                    account.balance -= amount
                    destination_account.balance += amount
                    account.save()
                    destination_account.save()
                    Transaction.objects.create(
                        account=account,
                        type="transfer",
                        amount=amount
                    )
                    Transaction.objects.create(
                        account=destination_account,
                        type="deposit",
                        amount=amount
                    )
                    messages.success(request, "Transfer Successful!")
                    return redirect("dashboard")
                else:
                    messages.error(request, "Oops! Insufficient Balance")
            except Account.DoesNotExist:
                messages.error(request, "Destination account does not exist.")
        else:
            messages.error(request, 'Something Went Wrong.')
    else:
        form = TransferForm()

    context = {"form": form}
    return render(request, "transfer.html", context)

@login_required(login_url="index")
def balance(request):
    account = get_object_or_404(Account, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-transaction_date')

    myFilter = TransactionFilter(request.GET, queryset=transactions)
    transactions = myFilter.qs
    context = {'account':account, 'transactions':transactions, 'myFilter':myFilter}

    return render(request, "balance.html", context)


