from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.user.username} - {self.account_number}'
    
class Transaction(models.Model):
    TRANSCTION_TYPE = [
        ('withdraw', 'withdraw'),
        ('deposit', 'deposit'),
        ('transfer', 'transfer')
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    type = models.CharField(max_length=10, choices=TRANSCTION_TYPE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    destination_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfer', null=True, blank=True)

    def __str__(self):
        return f'{self.type} - {self.amount} - {self.account.user.username}'


    
