from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Transaction

from .models import Account
import random
import string

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create the associated Account
            account_number = self.generate_account_number(user.username)
            Account.objects.create(user=user, account_number=account_number)
        return user

    def generate_account_number(self, username):
        random_number = ''.join(random.choices(string.digits, k=8))
        return f'{username.upper()}{random_number}'


class DepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount"]

class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount"]

class TransferForm(forms.Form):
        amount = forms.DecimalField(max_digits=15, decimal_places=2)
        destination_account_number = forms.CharField(max_length=20)