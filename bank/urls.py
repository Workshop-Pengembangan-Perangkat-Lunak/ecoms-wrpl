from django.urls import path
from . import views
# app_name = 'bank'
urlpatterns = [
    path('dashboard/', views.index_views, name='home'),
    path('applications/<int:user_id>/', views.show_applications, name='apply'),
    path('topup/<int:user_id>', views.topup, name='topup'),
    path('create/<int:user_id>', views.create_transaction, name='create'),
]