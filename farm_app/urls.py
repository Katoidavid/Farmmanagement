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

from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from django.urls import path

from farm_management import settings
from . import views
from .forms import CustomLoginForm
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('shop/', views.products_page, name='product'),
    path('contact/', views.contact, name='contact'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('visitorsapi/', views.visitorsapi, name='visitorsapi'),
    path('mpesaapi/', views.mpesaapi, name='mpesaapi'),
    path('login/', views.login_view, name='login'),
    path('add_product/', views.add_product, name='add_product'),
    path('product/update/<int:id>/', views.update_product, name='update_product'),
    path('product/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('products/', views.product_list, name='products'),
    path('cart/', views.cart_view, name='cart'),  # Cart page under Purchase
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),  # Checkout page under Purchase
    path('accounts/login/', LoginView.as_view(
        template_name='login.html',
        authentication_form=CustomLoginForm
    ), name='login'),
] + [ path('accounts/logout/', LogoutView.as_view(), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)