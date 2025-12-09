"""
models.py
Data models for the Campaign Analytics application.

Defines:
- Objective: high-level marketing objective (e.g., awareness, engagement).
- Channel: a social media account owned by a business.
- Campaign: a marketing campaign that runs on a single channel with a budget and dates.
- Post: individual social posts that belong to a campaign.
- PostMetrics: aggregated metrics (impressions, likes, comments, shares, clicks) for each post.
"""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Channel(models.Model):
    """
    Social media channel that is tracked in the dashboard.

    Each channel belongs to a single Django user (owner) and stores the
    platform type (e.g., Instagram, TikTok) and handle that will appear
    in the UI. Campaigns reference a channel through a foreign key.
    """
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='channels',
        null=True,
        blank=True,          
    )
    name = models.CharField(max_length=100)
    platform_handle = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Objective(models.Model):
    """
    Represents a high-level marketing objective for a campaign
    (e.g., brand awareness, engagement, website traffic).

    This model is standalone and does not depend on other models.
    Campaigns reference an objective through a foreign key.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class Campaign(models.Model):
    """
    Marketing campaign running on a single channel.

    A campaign is linked to:
    - one Channel (where the content is published),
    - one Objective (what the campaign is trying to achieve).

    It stores name, start/end dates and budget, and serves as the parent
    for Post objects.
    """
    OBJECTIVE_CHOICES = [
        ('AWARENESS', 'Brand awareness'),
        ('TRAFFIC', 'Website traffic'),
        ('ENGAGEMENT', 'Engagement'),
        ('LEADS', 'Lead generation'),
    ]

    name = models.CharField(max_length=150)
    objective = models.ForeignKey(
        "Objective",
        on_delete=models.PROTECT,   
        related_name="campaigns",
    )
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name='campaigns',
    )
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.channel.name})"


class Post(models.Model):
    """
    Individual social media post that is part of a campaign.

    Stores basic content information (date, content type, caption, URL)
    and has a 1-to-1 relationship with PostMetrics to keep performance
    data separated from content.
    """
    CONTENT_TYPE_CHOICES = [
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video'),
        ('REEL', 'Reel'),
        ('STORY', 'Story'),
        ('CAROUSEL', 'Carousel'),
    ]

    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    post_date = models.DateField()
    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPE_CHOICES,
    )
    caption = models.TextField()
    url = models.URLField(blank=True)

    def __str__(self):
        return f"Post {self.id} - {self.campaign.name}"


class PostMetrics(models.Model):
    """
    Performance metrics for a single Post.

    Tracks impressions, likes, comments, shares, saves and clicks.
    Used by the campaign performance report to aggregate results
    across all posts in a campaign.
    """
    post = models.OneToOneField(
        Post,
        on_delete=models.CASCADE,
        related_name='metrics',
    )
    impressions = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    saves = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Metrics for {self.post}"