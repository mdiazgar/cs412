from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Channel, Campaign, Post, PostMetrics


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform_handle')


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'channel', 'objective', 'start_date', 'end_date', 'budget')
    list_filter = ('channel', 'objective')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'campaign', 'post_date', 'content_type')
    list_filter = ('campaign', 'content_type')


@admin.register(PostMetrics)
class PostMetricsAdmin(admin.ModelAdmin):
    list_display = ('post', 'impressions', 'likes', 'comments', 'shares', 'clicks')
