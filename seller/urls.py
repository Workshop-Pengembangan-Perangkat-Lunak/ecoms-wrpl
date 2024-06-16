from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.show_products, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_update'),
    path('product/update/<int:product_id>/', views.product_detail, name='product_detail'),
    path('transactions/', views.show_transactions, name='transactions'),
    path('transaction/update/<int:transaction_id>/', views.transaction_detail, name='transaction_update'),
    path('transaction/<int:transaction_id>/', views.transaction_detail, name='transaction_detail'),
    path('delete_product/', views.delete_product, name='delete_product'),
    path('delete_transaction/', views.delete_transaction, name='delete_transaction'),
    path('create_transaction/', views.create_transaction, name='create_transaction'),
    path('create_product/', views.create_product, name='create_product'),

        # Auth 
    path('register/', views.register_seller, name='register'),
    path('login/', views.login_seller, name='login'),
]
