from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'buyer'
# app_name = 'ecoms'
urlpatterns = [
    path('', views.show_products, name='home'),
    path('products/', views.show_specific_products, name='products'),
    path('product_detail/<int:pk>', views.show_product_detail, name='show_product_detail'),
    path('departments/', views.show_departments, name='departments'),
    # path('carts/', views.show_carts, name='carts'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('add_to_cart2/<int:pk>', views.add_to_cart2, name='add_to_cart2'),
    path('transactions/', views.show_transactions, name='transactions'),
    path('shop/', views.show_shop, name='shop'),
    path('cart/', views.show_cart, name='cart'),
    path('remove_from_cart/<int:pk>', views.remove_from_cart, name='remove_from_cart'),
    
    
    # Auth 
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    
    path('checkout/', views.checkout, name='checkout'),
    
    #profile
    path('dashboard/', views.show_dashboard, name='dashboard'),
    path('update_profile/<int:pk>', views.update_profile, name='update_profile')
    # path('shop_detail/', views.show_shop_detail, name='shop_detail'),
]
