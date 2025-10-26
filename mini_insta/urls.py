# File: mini_insta/urls.py
# Author: María Díaz Garrido
# Description: URL routes for the mini_insta app. Maps:
#   - '' → ProfileListView (named 'show_all_profiles')
#   - 'profile/<int:pk>/' → ProfileDetailView (named 'show_profile')\
    
from django.urls import path
from django.conf import settings
from .views import *
from . import views
from django.contrib.auth import views as auth_views

app_name = "mini_insta"

urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"), 
    path('show_all_profiles/', ProfileListView.as_view(), name="show_all_profiles"), 
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="show_profile"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="show_post"),
    path("profile/create_post", CreatePostView.as_view(), name="create_post"),
    path("profile/update", UpdateProfileView.as_view(), name="update_profile"),
    path("post/<int:pk>/delete", DeletePostView.as_view(), name="delete_post"),
    path("post/<int:pk>/update", UpdatePostView.as_view(), name="update_post"),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='profile_followers'),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='profile_following'),
    path('profile/feed', PostFeedListView.as_view(), name='profile_feed'),
    path('profile/search', SearchView.as_view(), name='profile_search'),
    path("create_profile/", CreateProfileView.as_view(), name="create_profile"),
    path("profile/<int:pk>/follow", FollowCreateView.as_view(), name="profile_follow"),
    path("profile/<int:pk>/delete_follow", FollowDeleteView.as_view(), name="profile_delete_follow"),
    path("post/<int:pk>/like", LikeCreateView.as_view(), name="post_like"),
    path("post/<int:pk>/delete_like", LikeDeleteView.as_view(), name="post_delete_like"),
    ##authorization-related URL
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='mini_insta:show_all_profiles'), name='logout'),

]