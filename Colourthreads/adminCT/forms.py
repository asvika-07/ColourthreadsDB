
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from adminCT.models import Stocks
from adminCT import models
from adminCT.models import Customers, cust_address, cust_phone_number

class SignUpForm(forms.Form):
    name=forms.CharField(max_length=255)
    email=forms.EmailField(max_length=255)
    password=forms.CharField(max_length=255,widget=forms.PasswordInput())


class SignUpFormPno(forms.Form):
    phonenumber=forms.CharField(max_length=10)

class SignUpFormAddress(forms.Form):
    address_1=forms.CharField(max_length=255)
    address_2=forms.CharField(max_length=255)
    city=forms.CharField(max_length=255)
    zipcode=forms.CharField(max_length=255)


class cust_LoginForm(forms.Form):
    email=forms.CharField(max_length=255)
    password=forms.CharField(max_length=255,widget=forms.PasswordInput())


class Add_AdminForm(forms.Form):
    name=forms.CharField(max_length=255)
    email=forms.EmailField(max_length=255)
    password=forms.CharField(max_length=255,widget=forms.PasswordInput())
    phonenumber=forms.CharField(max_length=10)

CATEGORY_CHOICES =(
    ("SILK SAREES", "SILK SAREES"),
    ("COTTON SAREES", "COTTON SAREES"),
    ("LINEN SAREES", "LINEN SAREES"),
    ("KURTIS", "KURTIS"),
    ("ETHNIC DRESSES", "ETHNIC DRESSES"),
    ("SHAWLS","SHAWLS")
)
  
class Add_StockForm(forms.Form):

    name=forms.CharField(max_length=255)
    category=forms.ChoiceField(choices=CATEGORY_CHOICES)
    quantity=forms.IntegerField()
    price=forms.FloatField()
    image=forms.ImageField()
    description=forms.CharField(max_length=255)

class Add_Cat_ImageForm(forms.Form):
    category=forms.ChoiceField(choices=CATEGORY_CHOICES)
    image=forms.ImageField()
  
