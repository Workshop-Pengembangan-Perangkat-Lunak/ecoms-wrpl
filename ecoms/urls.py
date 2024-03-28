from django.urls import path
from . import views
# app_name = 'ecoms'
urlpatterns = [
    path('', views.show_products, name='home'),
    path('products/', views.show_specific_products, name='products'),
    path('departments/', views.show_departments, name='departments'),
    # path('carts/', views.show_carts, name='carts'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('transactions/', views.show_transactions, name='transactions'),
    path('shop/', views.show_shop, name='shop'),
    path('cart/', views.show_cart, name='cart'),
    path('dashboard/', views.show_dashboard, name='dashboard'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('checkout/', views.checkout, name='checkout')
    # path('shop_detail/', views.show_shop_detail, name='shop_detail'),
]
