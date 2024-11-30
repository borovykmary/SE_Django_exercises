from django import forms
from .models import Product
from django.shortcuts import render

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'available']
