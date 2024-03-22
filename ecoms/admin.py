from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Customer)
admin.site.register(Department)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(TransactionDetail)
admin.site.register(Cart)