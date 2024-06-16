from django.urls import path
from . import views
app_name = 'supplier'
urlpatterns = [
    # path('/'),
    path('registersupplier/', views.registersupplier, name='registersupplier'),
    path('login/', views.login_supplier, name='login_supplier'),
    path('dashboard/', views.show_dashboard, name='dashboard'),
    path('product/create/', views.create_product, name='create_product'),
    path('product/update/<int:product_id>',
         views.update_product, name='update_product'),
    path('product/delete/<int:product_id>',
         views.delete_product, name='delete_product')
]
