import os.path
from http.client import HTTPResponse
from lib2to3.fixes.fix_input import context
from tkinter.tix import IMAGE

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django_daraja.mpesa.core import MpesaClient
from pyexpat.errors import messages
from rest_framework import status
from rest_framework.decorators import api_view

from farm_app.Serializers import VisitorSerializer
from farm_app.forms import VisitorsmessageForm
from farm_app.models import Visitorsmessage


# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    data = Visitorsmessage.objects.all()
    context = {'data': data}
    return render(request, 'about.html', context)


def resume(request):
    return render(request, 'login_register.html')

def services(request):
    return render(request, 'services.html')

def portfolio(request):
    return render(request, 'products.html')


def contact(request):
    if request.method == 'POST':
        form = VisitorsmessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('contact')
    else:
        form = VisitorsmessageForm()
    return render(request,'contact.html', {'form': form})


  # Ensure this is correctly imported


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


def mpesaapi(request):
    client = MpesaClient()
    phone_number = '0768432814'
    amount = 5
    account_refrence = 'eMobilis'
    transaction_description = 'payment for web dev'
    callback_url = 'https://darajambili.herokuapp.com/express-payment';
    response = client.stk_push(phone_number,amount,account_refrence,transaction_description,callback_url)
    return HttpResponse(response)





