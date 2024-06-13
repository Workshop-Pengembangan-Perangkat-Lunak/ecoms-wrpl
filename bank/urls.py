from django.urls import path
from . import views
app_name = 'bank'
urlpatterns = [
    # path('', views.show_applications, name='home'),
    path('applications/<int:user_id>/', views.show_applications, name='apply'),
    path('create/', views.create_transaction, name='create_transaction'),
]