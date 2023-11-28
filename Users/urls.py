from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('purchase_item/', views.purchase_item, name='purchase_item'),
    path('home/',views.home,name='home'),
]
