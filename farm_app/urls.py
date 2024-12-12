"""
URL configuration for portfolioweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from xml.etree.ElementInclude import include

from django.contrib import admin

from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),  # This handles the root URL ("/")
    path('about/', views.about, name='about'),
    path('login_register/', views.resume, name='login'),
    path('services/', views.services, name='services'),
    path('shop/', views.portfolio, name='shop'),
    path('contact/', views.contact, name='contact'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('visitorsapi/', views.visitorsapi, name='visitorsapi'),
    path('mpesaapi/', views.mpesaapi, name='mpesaapi'),
]
