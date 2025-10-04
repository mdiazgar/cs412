# File: mini_insta/views.py
# Author: María Díaz Garrido
# Description: Class-based views for the mini_insta app. Provides:
#   - ProfileListView: lists all Profile records using show_all_profiles.html
#   - ProfileDetailView: displays a single Profile using show_profile.html

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from .forms import CreatePostForm

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
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["photos"] = self.object.get_all_photos()
        return ctx
    
class CreatePostView(CreateView):
    template_name = "mini_insta/create_post_form.html"
    form_class = CreatePostForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = get_object_or_404(Profile, pk=self.kwargs["pk"])
        return ctx

    def form_valid(self, form):
        profile = get_object_or_404(Profile, pk=self.kwargs["pk"])

        post = form.save(commit=False)
        post.profile = profile
        post.save()

        image_url = (self.request.POST.get("image_url") or "").strip()
        if image_url:
            Photo.objects.create(post=post, image_url=image_url)

        self.object = post
        return super().form_valid(form)  

    def get_success_url(self):
        # Use the object created in form_valid
        return reverse("mini_insta:show_post", kwargs={"pk": self.object.pk})
