from django import forms
from django.contrib.auth.forms import AuthenticationForm

from farm_app.models import Visitorsmessage, Product


class VisitorsmessageForm(forms.ModelForm):
    class Meta:
        model = Visitorsmessage
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Phone Number'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Gender'}),
           # 'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Age'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Subject'}),
            'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Message'}),
           # 'image': forms.ClearableFileInput(attrs={'class':'form-control','accept':'images/*','title': 'Upload your Image'})
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'image']

# authentication
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        }),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
        label='Password'
    )

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=15)
    email = forms.EmailField()


