from django.db import models

# Create your models here.

class Contacts(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 50, default= "")
    phone = models.CharField(max_length = 50, default = "")
    email = models.CharField(max_length = 200, default = "")

    # Predefine verbose name to avoid "Conctactss"
    class Meta:
        verbose_name_plural = "Contacts"

class Customers(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 50, default = "Customer name")
    email = models.CharField(max_length = 200, default = "")
    address = models.CharField(max_length = 50, default = "")
    contact = models.ForeignKey(Contacts, on_delete = models.CASCADE)

    # Predefine verbose name to avoid "Customerss"
    class Meta:
        verbose_name_plural = "Customers"

class Orders(models.Model):
    uid = models.AutoField(primary_key=True)
    slug = models.CharField(max_length = 50, default = "")
    project = models.CharField(max_length = 50, default = "Project name")
    description = models.CharField(max_length = 500, default = "Description of requirements, notes, etc...")
    price = models.DecimalField(max_digits = 8, decimal_places = 2, default = 0.00)
    customer = models.ForeignKey(Customers, on_delete = models.CASCADE)

    # Predefine verbose name to avoid "Orderss"
    class Meta:
        verbose_name_plural = "Orders"
