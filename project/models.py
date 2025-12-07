from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Channel(models.Model):
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
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class Campaign(models.Model):
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