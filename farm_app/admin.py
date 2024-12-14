# from django.contrib import admin
#
# from farm_app.models import Visitorsmessage
#
# # Register your models here.
# admin.site.register(Visitorsmessage)

from django.contrib import admin
from .models import Visitorsmessage, Product


@admin.register(Visitorsmessage)
class VisitorsMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone_number', 'gender', 'subject', 'message')


# admin.py
from django.contrib import admin
from .models import Product

admin.site.register(Product)
