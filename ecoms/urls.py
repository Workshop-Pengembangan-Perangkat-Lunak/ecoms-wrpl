from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.show_products, name='products'),
    path('departments/', views.show_departments, name='departments'),
    path('carts/', views.show_carts, name='carts'),
    path('add_to_carts/', views.add_to_cart, name='add_to_carts'),
    path('transactions/', views.show_transactions, name='transactions'),
    path('shop/', views.show_shop, name='shop'),
    path('cart/', views.show_cart, name='cart'),
    path('dashboard/', views.show_dashboard, name='dashboard'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login')
    # path('shop_detail/', views.show_shop_detail, name='shop_detail'),
]
