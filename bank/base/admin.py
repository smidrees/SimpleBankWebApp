from django.contrib import admin

# Register your models here.
from .models import Account, Transaction


class AccountAdmin(admin.ModelAdmin):
    list_display = ("user","account_number","balance")
    
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("account","amount","type","destination_account","transaction_date")

admin.site.register(Account,AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)