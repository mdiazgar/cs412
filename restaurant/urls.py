from django.urls import path
from django import settings
from django import static
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('', views.main, name='restaurant-home'),
    path('main/', views.main, name='main'),
    path('order/', views.order, name='order'),
    path('confirmation/', views.confirmation, name='confirmation'),
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)