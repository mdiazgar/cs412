# File: mini_insta/views.py
# Author: María Díaz Garrido
# Description: Class-based views for the mini_insta app. Provides:
#   - ProfileListView: lists all Profile records using show_all_profiles.html
#   - ProfileDetailView: displays a single Profile using show_profile.html

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth import login
from .forms import CreatePostForm, UpdateProfileForm, CreateProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .mixins import AuthProfileMixin, CurrentUserProfileObjectMixin


from .models import Profile, Post, Photo, Follow, Like
# from .forms import CreateArticleForm, CreateCommentForm
from django.urls import reverse
# Create your views here.

def _next_or(request, fallback_url):
    nxt = request.GET.get("next") or request.POST.get("next")
    return nxt or fallback_url

class ProfileListView(ListView):
    '''Define a view class to show all profiles'''
    
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"
    
    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''
 
 
        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')
 
        return super().dispatch(request, *args, **kwargs)
    
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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        me = getattr(self.request.user, "profiles", None)
        me = me.first() if me else None
        post = self.object
        ctx["current_profile"] = me
        ctx["liked_by_me"] = (
            bool(me) and post.likes.filter(profile=me).exists()
        )
        return ctx
    
class CreatePostView(AuthProfileMixin, CreateView):
    template_name = "mini_insta/create_post_form.html"
    form_class = CreatePostForm
    model = Post

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = self.get_current_profile()   # or get_current_profile()
        return ctx


    def form_valid(self, form):
        profile = self.get_current_profile()

        post = form.save(commit=False)
        post.profile = profile
        post.save()

        files = self.request.FILES.getlist("files")
        for f in files:
            Photo.objects.create(post=post, image_file=f)

        image_url = (self.request.POST.get("image_url") or "").strip()
        if image_url:
            Photo.objects.create(post=post, image_url=image_url)

        self.object = post
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("mini_insta:show_post", kwargs={"pk": self.object.pk})
    
class UpdateProfileView(CurrentUserProfileObjectMixin, UpdateView):
    model = Profile
    template_name = "mini_insta/update_profile_form.html"
    form_class = UpdateProfileForm
    
    def get_login_url(self):
        return reverse('login')
    

class DeletePostView(AuthProfileMixin, DeleteView):
    model = Post
    template_name = "mini_insta/delete_post_form.html"
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["post"] = self.object
        ctx["profile"] = self.object.profile
        return ctx

    def get_success_url(self):
        return reverse("mini_insta:show_profile", kwargs={"pk": self.object.profile.pk})

class UpdatePostView(AuthProfileMixin, UpdateView):
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
    

class PostFeedListView(AuthProfileMixin, ListView):
    """Feed for a single Profile"""
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        profile = self.get_current_profile()
        # Use your existing accessor that builds the feed:
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['profile'] = self.profile
        return ctx
    

class SearchView(AuthProfileMixin, ListView):
    """Search Profiles and Posts on behalf of a given Profile"""
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts' 

    def dispatch(self, request, *args, **kwargs):
        self.profile = self.get_current_profile()
        self.query = (request.GET.get("q") or "").strip()

        if not self.query:
            return render(request, "mini_insta/search.html", {"profile": self.profile})

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if not self.query:
            return Post.objects.none()
        return (Post.objects
                .filter(caption__icontains=self.query)
                .select_related("profile")
                .order_by("-published"))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profiles = Profile.objects.none()
        if self.query:
            profiles = Profile.objects.filter(
                Q(username__icontains=self.query) |
                Q(display_name__icontains=self.query) |
                Q(bio_text__icontains=self.query)
            ).order_by("display_name", "username")

        ctx.update({
            "profile": self.profile,
            "query": self.query,
            "profiles": profiles,
        })
        return ctx
    
    
class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault("user_form", UserCreationForm())
        return ctx

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if not user_form.is_valid():
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))
        user = user_form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        form.instance.user = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("mini_insta:show_profile", args=[self.object.pk])
    
    
class FollowCreateView(AuthProfileMixin, CreateView):
    def post(self, request, pk):
        me = self.get_current_profile()
        other = get_object_or_404(Profile, pk=pk)
        if other.pk != me.pk: 
            Follow.objects.get_or_create(profile=other, follower_profile=me)
        return redirect(_next_or(request, other.get_absolute_url()))

    def get(self, request, pk):
        return self.post(request, pk)


class FollowDeleteView(AuthProfileMixin, DeleteView):
    def post(self, request, pk):
        me = self.get_current_profile()
        other = get_object_or_404(Profile, pk=pk)
        Follow.objects.filter(profile=other, follower_profile=me).delete()
        return redirect(_next_or(request, other.get_absolute_url()))

    def get(self, request, pk):
        return self.post(request, pk)


class LikeCreateView(AuthProfileMixin, CreateView):
    def post(self, request, pk):
        me = self.get_current_profile()
        post = get_object_or_404(Post, pk=pk)
        if post.profile_id != me.pk:
            Like.objects.get_or_create(post=post, profile=me)
        return redirect(request.POST.get("next") or post.get_absolute_url())

    def get(self, request, pk):
        return self.post(request, pk)
    

class LikeDeleteView(AuthProfileMixin, DeleteView):
    def post(self, request, pk):
        me = self.get_current_profile()
        post = get_object_or_404(Post, pk=pk)
        Like.objects.filter(post=post, profile=me).delete()
        return redirect(request.POST.get("next") or post.get_absolute_url())

    def get(self, request, pk):
        return self.post(request, pk)