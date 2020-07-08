from django.urls import path
from app_order import views


app_name = 'app_order'

urlpatterns = [
    path('add/<pk>/', views.add_to_cart, name='add')
]
