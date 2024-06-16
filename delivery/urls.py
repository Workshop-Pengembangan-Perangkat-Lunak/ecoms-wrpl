from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('user_deliveries/', views.user_deliveries, name='user_deliveries'),
    path('add_delivery/', views.add_delivery, name='add_delivery'),

        # Auth 
    path('register/', views.register_user, name='delivery_register'),
    path('login/', views.login_user, name='delivery_login'),
    path('logout/', views.logout_user, name='logout'),

]
