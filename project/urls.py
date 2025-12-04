from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('', views.ChannelListView.as_view(), name='channel_list'),
    path('channels/<int:pk>/', views.ChannelDetailView.as_view(), name='channel_detail'),

    path('campaigns/', views.CampaignListView.as_view(), name='campaign_list'),
    path('campaigns/<int:pk>/', views.CampaignDetailView.as_view(), name='campaign_detail'),
    path('campaigns/create/', views.CampaignCreateView.as_view(), name='campaign_create'),

    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),
]
