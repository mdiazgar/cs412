# File: mini_insta/views.py
# Author: María Díaz Garrido
# Description: Class-based views for the mini_insta app. Provides:
#   - ProfileListView: lists all Profile records using show_all_profiles.html
#   - ProfileDetailView: displays a single Profile using show_profile.html

from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from .models import Profile, Post, Photo
# from .forms import CreateArticleForm, CreateCommentForm
from django.urls import reverse
# Create your views here.

class ProfileListView(ListView):
    '''Define a view class to show all profiles'''
    
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"
    
class ProfileDetailView(DetailView):
    '''Defining the individual profiles'''
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"
    
class PostDetailView(DetailView):
    '''A view to handle the creation of a new article
    1) Display the HTML for to user (GET)
    2) Process the form submission and store the new Article object (POST)'''
    model = Post
    template_name = "mini_insta/show_post.html"  # required name
    context_object_name = "post"
    
# class CreateCommentView(CreateView):
#     '''A view to handle creation of a new Comment on an Article'''
#     form_class = CreateCommentForm
#     template_name = 'blog/create_comment_form.html'
    
#     def get_success_url(self):
#         '''Provide a URL to redirect to after creating a new Comment'''
#         #create and return URL
#         return reverse('show_all')
