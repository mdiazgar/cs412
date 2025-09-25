from django.urls import path
from django.conf import settings
from .views import ProfileListView
from . import views

app_name = "mini_insta"

urlpatterns = [
    path('', views.ProfileListView.as_view(), name="show_all_profiles"), 
    
]