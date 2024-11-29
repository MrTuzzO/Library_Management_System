from django.contrib import admin
from transactions.models import Transaction, BorrowHistory

admin.site.register(Transaction)
admin.site.register(BorrowHistory)
