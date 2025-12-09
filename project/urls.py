"""
urls.py

URL configuration for the Campaign Analytics application.
Maps human-readable URLs to view functions and class-based views.
"""

from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('', views.ChannelListView.as_view(), name='channel_list'),
    path('channels/<int:pk>/', views.ChannelDetailView.as_view(), name='channel_detail'),

    path('campaigns/', views.CampaignListView.as_view(), name='campaign_list'),
    path('campaigns/create/', views.CampaignCreateView.as_view(), name='campaign_create'),
    path('campaigns/<int:pk>/', views.CampaignDetailView.as_view(), name='campaign_detail'),
    path('campaigns/<int:pk>/edit/', views.CampaignUpdateView.as_view(), name='campaign_update'),

    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    path('reports/campaign-performance/', views.campaign_performance_report, name='campaign_performance_report'),

]
