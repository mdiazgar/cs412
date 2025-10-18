# File: mini_insta/views.py
# Author: María Díaz Garrido
# Description: Class-based views for the mini_insta app. Provides:
#   - ProfileListView: lists all Profile records using show_all_profiles.html
#   - ProfileDetailView: displays a single Profile using show_profile.html

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreatePostForm, UpdateProfileForm

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
    '''A view to handle the creation of a new post
    1) Display the HTML for to user (GET)
    2) Process the form submission and store the new Post object (POST)'''
    model = Post
    template_name = "mini_insta/show_post.html"  
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

        # create Post
        post = form.save(commit=False)
        post.profile = profile
        post.save()

        files = self.request.FILES.getlist('files')  
        for f in files:
            Photo.objects.create(post=post, image_file=f)
            
        image_url = (self.request.POST.get("image_url") or "").strip()
        if image_url:
            Photo.objects.create(post=post, image_url=image_url)

        self.object = post
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("mini_insta:show_post", kwargs={"pk": self.object.pk})
    
class UpdateProfileView(UpdateView):
    model = Profile
    template_name = "mini_insta/update_profile_form.html"
    form_class = UpdateProfileForm
    

class DeletePostView(DeleteView):
    model = Post
    template_name = "mini_insta/delete_post_form.html"
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["post"] = self.object
        ctx["profile"] = self.object.profile
        return ctx

    def get_success_url(self):
        return reverse("mini_insta:show_profile", kwargs={"pk": self.object.profile.pk})

class UpdatePostView(UpdateView):
    model = Post
    template_name = "mini_insta/update_post_form.html"
    fields = ["caption"] 

    def get_success_url(self):
        return reverse("mini_insta:show_post", kwargs={"pk": self.object.pk})
    

class ShowFollowersDetailView(DetailView):
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile' 
    
class ShowFollowingDetailView(DetailView):
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'
    

class PostFeedListView(ListView):
    """Feed for a single Profile"""
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.profile = Profile.objects.get(pk=self.kwargs['pk'])
        return self.profile.get_post_feed(include_self=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['profile'] = self.profile
        return ctx
    

class SearchView(ListView):
    """Search Profiles and Posts on behalf of a given Profile"""
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts' 

    def dispatch(self, request, *args, **kwargs):
        self.profile = Profile.objects.get(pk=kwargs['pk'])
        self.query = (request.GET.get('q') or '').strip()
        if not self.query:
            return render(request, 'mini_insta/search.html', {'profile': self.profile, 'query': self.query})

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return (Post.objects.filter(caption__icontains=self.query).select_related('profile').order_by('-published'))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        by_username     = Profile.objects.filter(username__icontains=self.query)
        by_display_name = Profile.objects.filter(display_name__icontains=self.query)
        by_bio          = Profile.objects.filter(bio_text__icontains=self.query)
        profiles_qs = (by_username | by_display_name | by_bio).distinct().order_by('display_name', 'username')

        ctx.update({
            'profile': self.profile,     
            'query': self.query,         
            'profiles': profiles_qs,     
            'posts': ctx.get('posts'),   
        })
        return ctx