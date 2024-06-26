import django_filters
from .models import Transaction

import django_filters
from django_filters import DateFilter
from .models import Transaction

class TransactionFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='transaction_date', lookup_expr='gte')
    end_date = DateFilter(field_name='transaction_date', lookup_expr='lte')
    class Meta:
        model = Transaction
        fields = {
            'amount',  # Optional: add filtering for greater than or equal, less than or equal
            'type',
        }


# class TransactionFilter(django_filters.FilterSet):
#     class Meta:
#         model = Transaction
#         fields = {
#             'amount': ['exact', 'gte', 'lte'],  # Optional: add filtering for greater than or equal, less than or equal
#             'type': ['exact'],
#             'transaction_date': ['exact', 'gte', 'lte'],  # Optional: add filtering for date ranges
#         }
