# quotes/urls.py
from django.urls import path
from django import settings
from django import static
from . import views
app_name = 'quotes'
urlpatterns = [
    path('', views.quote, name='quote-home'),
    path('quote/', views.quote, name='quote'),
    path('show_all/', views.show_all, name='show_all'),
    path('about/', views.about, name='about'),
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)