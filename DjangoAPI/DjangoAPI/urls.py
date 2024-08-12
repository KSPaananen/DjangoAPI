"""
URL configuration for DjangoAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from App.views import UsersControlView, UsersAuthView, UsersLogOutView, ContactsViewSet, customersList, customersDetails, \
     customersCreate, ListCreateOrdersView, RetrieveUpdateDestroyOrdersViewSlug, RetrieveUpdateDestroyOrdersViewUID

# How to route using routers
router = SimpleRouter()
router.register("contacts", ContactsViewSet, basename="Contacts")

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("api/auth/register/", UsersControlView.as_view()),
    path("api/auth/login/", UsersAuthView.as_view()),
    path("api/auth/logout/", UsersLogOutView.as_view()),

    path("api/", include(router.urls)),

    path("api/customers/", customersList),
    path("api/customers/create/", customersCreate),
    path("api/customers/<int:pk>/", customersDetails),

    path("api/orders/", ListCreateOrdersView.as_view(), name = "Orders-List"),
    path("api/orders/<slug>/", RetrieveUpdateDestroyOrdersViewSlug.as_view(), name = "Orders-RetrieveSlug"),
    path("api/orders/<pk>/", RetrieveUpdateDestroyOrdersViewUID.as_view(), name = "Orders-RetrieveUID"),

]
