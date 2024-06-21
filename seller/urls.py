from django.urls import path
from . import views
app_name = 'seller'

urlpatterns = [
    path('dashboard/', views.show_dashboard, name='dashboard'),
    path('products/', views.show_products, name='products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/update/<int:product_id>/', views.update_product, name='product_update_seller'),
    path('delete_product/<int:product_id>', views.delete_product, name='delete_product_seller'),
    path('transactions/', views.show_transactions, name='transactions'),
    path('transactions/update/<int:transaction_id>/', views.transaction_detail, name='transaction_update'),
    path('transactions/<int:transaction_id>/', views.transaction_detail, name='transaction_detail'),
    
    path('delete_transaction/', views.delete_transaction, name='delete_transaction'),
    path('create_transaction/', views.create_transaction, name='create_transaction'),
    path('create_product/', views.create_product, name='create_product'),
    path('get_product/', views.get_product, name='get_product'),

        # Auth 
    path('register/', views.register_seller, name='register_seller'),
    path('login/', views.login_seller, name='login_seller'),
    path('logout/', views.logout_seller, name='logout_seller'),
]
