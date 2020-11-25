"""RautsApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from RautsApp_app import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/',obtain_auth_token),

    path('users/', views.users),
    path('users/<int:id>', views.users),

    path('vehicles', views.vehicles),
    path('vehicles/<int:id>', views.vehicles),

    path('vehicledoc/', views.vehicleDocument),
    path('vehicledoc/<int:id>', views.vehicleDocument),

    path('userdetails/', views.userDetails),
    path('userdetails/<int:id>', views.userDetails),

    path('distributor/', views.distributor),
    path('distributor/<int:id>', views.distributor),

    path('distributor-insurance/', views.distributorInsurance),
    path('distributor-insurance/<int:id>', views.distributorInsurance),
]
