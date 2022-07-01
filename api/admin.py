from django.contrib import admin

from .models import transaction, customer

# Register your models here.

admin.site.register(customer)
admin.site.register(transaction)