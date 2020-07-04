from django.shortcuts import render

# import views
from django.views.generic import ListView, DetailView

# models
from app_shop.models import Product, Category


class Home(ListView):
    model = Product
    template_name = 'app_shop/home.html'