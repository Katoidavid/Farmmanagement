from django import forms

from farm_app.models import Visitorsmessage


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