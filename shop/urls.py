# shop/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<str:sku>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<str:sku>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    
	path('order-success/', views.order_success, name='order_success'),
]
