# File: mini_insta/urls.py
# Author: María Díaz Garrido
# Description: URL routes for the mini_insta app. Maps:
#   - '' → ProfileListView (named 'show_all_profiles')
#   - 'profile/<int:pk>/' → ProfileDetailView (named 'show_profile')\
    
from django.urls import path
from django.conf import settings
from .views import ProfileListView
from .views import ProfileDetailView
from . import views

app_name = "mini_insta"

urlpatterns = [
    path('', views.ProfileListView.as_view(), name="show_all_profiles"), 
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="show_profile")
]