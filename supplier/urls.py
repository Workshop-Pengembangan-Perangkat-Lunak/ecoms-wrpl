from django.urls import path
from . import views
app_name = 'supplier'
urlpatterns = [
    # path('/'),
    path('registersupplier/', views.registersupplier, name='registersupplier'),
    path('login/', views.login_supplier, name='login_supplier'),
    path('dashboard/', views.show_dashboard, name='dashboard')
]
