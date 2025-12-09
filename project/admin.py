"""
admin.py

Admin configuration for the Campaign Analytics application.

Registers Channel, Campaign, Post, PostMetrics and Objective models in the
Django admin site with customised list displays, filters and search fields.
This makes it easier to inspect and manage data while developing, testing
and grading the project.
"""

from django.contrib import admin
from .models import Channel, Campaign, Post, PostMetrics, Objective


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    """
    Admin configuration for Channel.

    Displays the channel's name and handle in the list view so instructors
    can quickly see which social accounts exist in the system.
    """
    list_display = ("name", "platform_handle")


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    """
    Admin configuration for Campaign.

    Shows key campaign fields (channel, objective, dates and budget) and
    provides list filters by channel and objective to quickly slice data.
    """
    list_display = ("name", "channel", "objective", "start_date", "end_date", "budget")
    list_filter = ("channel", "objective")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for Post.

    Lists posts by campaign, date and content type and allows filtering
    by campaign or content type to review specific subsets of posts.
    """
    list_display = ("id", "campaign", "post_date", "content_type")
    list_filter = ("campaign", "content_type")


@admin.register(PostMetrics)
class PostMetricsAdmin(admin.ModelAdmin):
    """
    Admin configuration for PostMetrics.

    Exposes impressions, likes, comments, shares and clicks for each post
    so performance data can be checked or edited directly from the admin.
    """
    list_display = ("post", "impressions", "likes", "comments", "shares", "clicks")


@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    """
    Admin configuration for Objective.

    Shows the objective name and slug, and enables search on both fields
    to quickly locate a specific marketing objective.
    """
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
