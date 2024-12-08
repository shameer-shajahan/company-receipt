# delivery_receipt/forms.py

from django import forms
from .models import DeliveryReceipt, Item
from django.contrib.auth.forms import UserCreationForm
from rcp.models import User

# forms.py

from django import forms
from .models import DeliveryReceipt

class DeliveryReceiptForm(forms.ModelForm):
    class Meta:
        model = DeliveryReceipt
        fields = ['company_name', 'company_address', 'email', 'phone_number', 'delivery_address', 'delivery_boy', 'receiver_signature', 'delivery_boy_signature']

    # Add custom classes to form fields
    company_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    company_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    delivery_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    delivery_boy = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    receiver_signature = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    delivery_boy_signature = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['serial_number', 'item_description', 'quantity', 'uom', 'remarks']

class SignUpForm(UserCreationForm):

    class Meta:

        model=User

        fields=["username","email","phone","password1","password2"]

        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "password1":forms.TextInput(attrs={"class":"form-control"}),
            "password2":forms.TextInput(attrs={"class":"form-control"}),
            "phone":forms.NumberInput(attrs={"class":"form-control"}),
            
                 }      


class SignInForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

    password=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))


    