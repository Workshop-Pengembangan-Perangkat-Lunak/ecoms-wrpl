from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.show_products, name='products'),
    path('departments/', views.show_departments, name='departments'),
    path('carts/', views.show_carts, name='carts'),
    path('add_to_carts/', views.add_to_cart, name='add_to_carts'),
    path('transactions/', views.show_transactions, name='transactions'),
    path('users/', views.show_users, name='users'),
    path('users/<int:id>', views.show_specific_user, name='spec_user'),
    path('users/<int:id>/cart', views.show_user_cart, name='user_cart'),
    path('users/<int:id>/transactions', views.show_user_trans, name='user_trans'),
    path('shop/', views.show_shop, name='shop'),
    path('cart/', views.show_cart, name='cart'),
    # path('shop_detail/', views.show_shop_detail, name='shop_detail'),
]
