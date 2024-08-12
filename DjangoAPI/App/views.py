from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from .models import Orders, Customers, Contacts
from .serializers import UsersSerializer, OrdersSerializer, CustomersSerializer, ContactsSerializer

# --- User control --- #
class UsersControlView(APIView):
    serializer_class = UsersSerializer
    http_method_names = ["post"]

    # User registering. UsersSerializer takes care of duplicate prevention and password hashing
    def post(self, request):
       serializer = UsersSerializer(data = request.data)
       
       # Verify data
       if not serializer.is_valid():
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
       # Save user
       serializer.save()

       # Get user with hashed password for token creation
       user = User.objects.get(username=request.data["username"], email=request.data["email"])

       token = Token.objects.create(user=user)

       return Response({"token": token.key, "user": {"username": user.username, "email": user.email}}, status=status.HTTP_201_CREATED)

class UsersAuthView(APIView):
    serializer_class = UsersSerializer
    http_method_names = ["post"]

    # Login can executed with either username or email
    def post(self, request):
        user = get_object_or_404(User, username = request.data["username"], email = request.data["email"])
        if not user.check_password(request.data["password"]):
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        token, created = Token.objects.get_or_create(user = user)
        serializer = UsersSerializer(instance = user)
        
        return Response({"token": token.key, "user": {"username": user.username, "email": user.email}}, status=status.HTTP_200_OK)
    
class UsersLogOutView(APIView):
    http_method_names = ["delete"]

    def delete(self, request):
        tokenValue = request.data["token"]

        if not tokenValue:
            return Response({"detail": "Token not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = Token.objects.get(key = tokenValue)
            token.delete()
            return Response({"detail": "Token deleted successfully."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "Token does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        
"""
    Keep in mind:
    - Orders were made using generic views
    - Customers were made using function based views
    - Contacts were made using Viewsets
"""

# --- Orders --- #
class ListCreateOrdersView(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)

        if not serializer.is_valid():
           return Response({'error': 'request contains empty fields'}, status=status.HTTP_400_BAD_REQUEST)

        slug = request.data.get("slug")
        project = request.data.get("project")
        description = request.data.get("description")
        price = request.data.get("price")
        
        if Orders.objects.filter(slug = slug, project = project, description = description, price = price).exists():
            return Response({'error': 'Order already exists'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# Retrieve using a term
class RetrieveUpdateDestroyOrdersViewSlug(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    lookup_field = "slug"

# Retrieve using a primary key
class RetrieveUpdateDestroyOrdersViewUID(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


# --- Customers --- #
# Get all customers
@api_view(["GET"])
def customersList(request):
    queryset = Customers.objects.all()
    serializer = CustomersSerializer(queryset, many=True)
    return Response(serializer.data)

# Create a new customer
@api_view(["POST"])
def customersCreate(request):
    serializer = CustomersSerializer(data = request.data)
    if not serializer.is_valid():
        return Response({'error': 'request contains empty fields'}, status=status.HTTP_400_BAD_REQUEST)
    
    name = request.data.get("name")
    email = request.data.get("email")
    address = request.data.get("address")

    if Customers.objects.filter(name = name, email = email, address = address).exists():
        return Response({'error': 'Customer already exists'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# Get singular, update or delete an existing customer
@api_view(["GET", "PUT", "DELETE"])
def customersDetails(request, pk):
    try:
        queryset = Customers.objects.get(pk = pk)
    except Customers.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        queryset = Customers.objects.get(pk = pk)
        serializer = CustomersSerializer(queryset)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CustomersSerializer(queryset, data = request.data)
        if not serializer.is_valid():
            return Response({'error': 'data is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- Contacts --- #
class ContactsViewSet(viewsets.ModelViewSet):
    serializer_class = ContactsSerializer
    queryset = Contacts.objects.all()
    
    def list(self, request):
        serializer = self.get_serializer(self.queryset, many = True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        contact = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(contact)
        return Response(serializer.data)

    def create(self, request):
       serializer = self.get_serializer(data=request.data)
       
       # Verify data
       if not serializer.is_valid():
           return Response({'error': 'request contains empty fields'}, status=status.HTTP_400_BAD_REQUEST)
       
       # Make sure not to create duplicates
       name = request.data.get("name")
       phone = request.data.get("phone")
       email = request.data.get("email")
       
       if Contacts.objects.filter(name=name, phone=phone, email=email).exists():
           return Response({'error': 'Contact already exists'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
       else:
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       
    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return Response.Response(status=status.HTTP_200_OK)
