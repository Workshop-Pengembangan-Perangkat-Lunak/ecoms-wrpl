from django.urls import path
from . import views

urlpatterns = [
    path('/'),
    path('/register', views.register_supllier, name='register'),
    path('/login', views.login_supplier, name='register'),
    path('/dashboard', views.show_dashboard, name='dashboard')
]
