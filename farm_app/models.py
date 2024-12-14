from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from decimal import Decimal
from django.db import models


# Create your models here.
# class Visitorsmessage(models.Model):
#     #image = models.ImageField(upload_to='portfolio_images/', blank=True)
#     name = models.CharField(max_length=25)
#     email= models.EmailField(max_length=30)
#     phone_number = models.IntegerField()
#     gender= models.CharField(max_length=18)
#     #age=models.IntegerField()
#     subject = models.CharField(max_length=200)
#     message = models.TextField()
#
#     def __str__(self):
#         return self.name

class Visitorsmessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.subject}"
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)  # Track stock quantity
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - KSh {self.price:,.2f}"

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])


# Cart
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def get_total_price(self):
        # Calculate total price by summing up all items' total prices
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Reference existing Product model
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    def get_total_price(self):
        return self.product.price * Decimal(self.quantity)

