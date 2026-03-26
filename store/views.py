# Create your views here.

from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import ListView
from .models import Product

def index(request):
    return HttpResponse("Hello, world! You've reached still unnamed store's homepage!")

class HomeView(ListView):
    model = Product
    template_name = "home.html"

class ProductView(ListView):
    model = Product
    template_name = "product.html"
