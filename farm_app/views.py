import os.path
from http.client import HTTPResponse
from lib2to3.fixes.fix_input import context
from tkinter.tix import IMAGE

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django_daraja.mpesa.core import MpesaClient
from pyexpat.errors import messages
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem, Product
from django.shortcuts import render, redirect
from .forms import CheckoutForm
from django.contrib import messages

from farm_app.Serializers import VisitorSerializer
from farm_app.forms import VisitorsmessageForm, ProductForm
from farm_app.models import Visitorsmessage, Product


# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    data = Visitorsmessage.objects.all()
    context = {'data': data}
    return render(request, 'about.html', context)


def products_page(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def contact(request):
    if request.method == 'POST':
        form = VisitorsmessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('contact')
    else:
        form = VisitorsmessageForm()
    return render(request,'contact.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_authenticated:
            login(request, user)
            # Redirect to the next page if provided in the URL, otherwise go to the home page
            next_url = request.GET.get('next', 'add_product')
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials.'})
    return render(request, 'login.html')

def update(request, id):
    visitormessage = get_object_or_404(Visitorsmessage, id=id)
    if request.method == 'POST':
        form = VisitorsmessageForm(request.POST, request.FILES, instance=visitormessage)
        if form.is_valid():
            form.save()

            if 'image' in request.FILES:
                file_name = os.path.basename(request.FILES['image'].name)
                messages.success(request, f'Viewer updated successfully! {file_name} uploaded')
            else:
                messages.success(request, 'Viewer details updated successfully.')
            return redirect('about')
        else:
            messages.error(request, 'Please confirm your changes')
    else:
        form = VisitorsmessageForm(instance=visitormessage)
    return render(request, 'update.html', {'form': form, 'visitormessage': visitormessage})

def delete(request,id):
    visitormessage = get_object_or_404(Visitorsmessage, id=id)

    try:
        visitormessage.delete()
        messages.success(request, 'Visitor Deleted Successfully')
    except Exception as e:
        messages.error(request, 'Visitor not Deleted!')
    return redirect('about')

def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('products')  # Redirect to the products page
    return render(request, 'delete_product.html', {'product': product})

def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('products')  # Redirect to the products page
    else:
        form = ProductForm(instance=product)
    return render(request, 'update_product.html', {'form': form, 'product': product})


@api_view(['GET','POST'])
def visitorsapi(request):
    if request.method == 'GET':
        visitors = Visitorsmessage.objects.all()
        serializer = VisitorSerializer(visitors, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        serializer =VisitorSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required(login_url='login')  # Redirect to login if not authenticated
@user_passes_test(is_admin, login_url='login')  # Redirect to login if not an admin
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')  # Redirect to products page after successful form submission
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


# mpesa integtration
def mpesaapi(request):
    client = MpesaClient()
    phone_number = '0768432814'
    amount = 5
    account_refrence = 'eMobilis'
    transaction_description = 'payment for web dev'
    callback_url = 'https://darajambili.herokuapp.com/express-payment';
    response = client.stk_push(phone_number,amount,account_refrence,transaction_description,callback_url)
    return HttpResponse(response)

#checkout view

def checkout_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total = sum(item.get_total_price() for item in cart_items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Here, handle the order creation and mark cart as purchased
            cart.delete()
            messages.success(request, "Your order has been placed successfully.")
            return redirect('home')
    else:
        form = CheckoutForm()

    context = {
        'cart_items': cart_items,
        'total': total,
        'form': form,
    }
    return render(request, 'checkout.html', context)

# fixed cart
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total = cart.get_total_price()

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, "Product added to cart!")
    return redirect('cart_view')

def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                messages.error(request, "Quantity must be at least 1.")
            else:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, "Cart updated successfully.")
        except ValueError:
            messages.error(request, "Invalid quantity entered.")

    return redirect('cart_view')

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart_view')

