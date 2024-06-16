from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(BankAccount)
admin.site.register(TopUpHistory)
admin.site.register(Application)
admin.site.register(TransactionHistory)
admin.site.register(BankAdmin)

