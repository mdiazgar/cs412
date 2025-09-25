from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile
# Create your views here.

class ShowAllView(ListView):
    '''Define a view class to show all blog Articles'''
    
    model = Profile
    template_name = "mini_insta/show_all.html"
    context_object_name = "profiles"
    