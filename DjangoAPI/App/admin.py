from django.contrib import admin
from App.models import Orders, Customers, Contacts

# Register your models here.

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    pass

@admin.register(Customers)
class OrdersAdmin(admin.ModelAdmin):
    pass

@admin.register(Contacts)
class OrdersAdmin(admin.ModelAdmin):
    pass