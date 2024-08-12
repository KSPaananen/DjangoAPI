from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import Orders, Customers, Contacts

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {
            'uid' : {
                'required' : False,
                'read_only': True
            },
            'username' : {
                'required' : True,
                'min_length': 3
            },
            'email' : {
                'required' : True,
                'min_length': 3
            },
            'password' : {
                'required' : True,
                'min_length': 3
            }
        }

    def create(self, validated_data):
        # Isolate data
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        # Check for duplicates
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            raise PermissionDenied("User already exists!")
        else:
            # Hash the password & create user
            password = make_password(password)
            user = User.objects.create(username=username, email=email, password=password)
        
        return user


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = "__all__"
        extra_kwargs = {
            'uid' : {
                'required' : False,
                'read_only': True
            },
            'name' : {
                'required' : True,
                'min_length': 3
            },
            'phone' : {
                'required' : True,
                'min_length': 3
            },
            'email' : {
                'required' : True,
                'min_length': 3
            }
        }

# This serializer enables the creation of a new contact whilst adding a customer
class CustomersSerializer(serializers.ModelSerializer):
    contact = ContactsSerializer()

    class Meta:
        model = Customers
        fields = "__all__"
        extra_kwargs = {
            'uid': {
                'required' : False,
                'read_only': True
            },
             'name' : {
                'required' : True,
                'min_length': 3
            },
            'email' : {
                'required' : True,
                'min_length': 3
            },
            'address' : {
                'required' : True,
                'min_length': 3
            },
            'contact' : {
                'required' : True
            }
        }

    def create(self, validated_data):
        contactData = validated_data.pop("contact")

        contact = Contacts.objects.create(**contactData)
        customer = Customers.objects.create(contact = contact, **validated_data)

        return customer

# This serializer handles"customer" as a single "uid" instead of a nested object
class OrdersSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset = Customers.objects.all())

    class Meta:
        model = Orders
        fields = ["uid", "slug", "project", "description", "price", "customer"]
        extra_kwargs = {
            'uid': {
                'required' : False,
                'read_only': True
            },
            'slug': {
                'required' : False,
            },
             'Project' : {
                'required' : True,
                'min_length': 3
            },
            'description' : {
                'required' : True,
                'min_length': 3
            },
            'price' : {
                'required' : True,
            },
            'customer' : {
                'required' : True,
            }
        }
