# File: mini_insta/models.py
# Author: María Díaz Garrido
# Description: Database models for the mini_insta app. Defines the Profile model
#              with username, display_name, bio_text, profile_image_url (URL),
#              and join_date (auto-updated). __str__ returns the username.


from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    "Encapsulate the data of a mini insta"
    
    #define the data attributes of the Mini_insta object
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="profiles") 
    
    username=models.TextField(blank=True)
    display_name=models.TextField(blank=True)
    bio_text=models.TextField(blank=True)
    profile_image_url=models.URLField(blank=True)
    join_date= models.DateTimeField(auto_now=True)
    
    def __str__(self):
        "Return a string representation of this model instance"
        return f'{self.username}' 
    
    def get_absolute_url(self):
        "Return a URL to display one instance of this object"
        return reverse("mini_insta:show_profile", kwargs={"pk": self.pk})
    
    def get_all_posts(self):
        "Return all posts for this profile"
        posts = Post.objects.filter(profile=self).order_by('-published')
        return posts
    
    def get_followers(self):
        """Return a LIST of Profile objects who follow this profile."""
        from .models import Follow
        qs = (Follow.objects.filter(profile=self).select_related('follower_profile'))         
        return [f.follower_profile for f in qs]                  

    def get_num_followers(self):
        """Return the COUNT of followers of this profile."""
        from .models import Follow
        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        """Return a LIST of Profile objects that this profile is following."""
        from .models import Follow
        qs = (Follow.objects.filter(follower_profile=self).select_related('profile'))
        return [f.profile for f in qs]                         

    def get_num_following(self):
        """Return the COUNT of profiles this profile follows."""
        from .models import Follow
        return Follow.objects.filter(follower_profile=self).count()
    
    def get_post_feed(self, include_self=False):
        """Return posts from the profiles this user follows"""
        from .models import Follow, Post  

        followed_ids = (Follow.objects.filter(follower_profile=self).values_list('profile_id', flat=True))
        qs = Post.objects.filter(profile_id__in=followed_ids)

        return (qs.select_related('profile').order_by('-published'))
    

    
class Post(models.Model):
    "Encapsulate the idea of a Post for a Profile"
    
    # data attributes for the Post:
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        "Return a string representation of this object"
        return f'{self.caption}'
    
    def get_all_photos(self):
        """Return all Photos for this post"""
        return Photo.objects.filter(post=self).order_by('-timestamp')
    
    def get_all_comments(self):
        """Return all comments for this post, newest first."""
        return self.comments.select_related('profile').order_by('-timestamp')
    
    def get_likes(self):
        """Return all Like rows for this post."""
        from .models import Like
        return (Like.objects.filter(post=self).select_related('profile').order_by('-timestamp'))
    
    def get_num_likes(self):
        """Return all number of Likes."""
        from .models import Like
        return Like.objects.filter(post=self).count()


    
class Photo(models.Model):
    "Encapsulates the idea of a Photo for a Post"
    
    # data attributes for the Photo:
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='photos')
    image_url  = models.URLField(blank=True)
    image_file = models.ImageField(upload_to='photos/', blank=True, null=True)
    timestamp  = models.DateTimeField(auto_now=True)

    def get_image_url(self):
        if self.image_url:
            return self.image_url
        if self.image_file:
            try:
                return self.image_file.url
            except ValueError:
                return ''
        return ''

    def __str__(self):
        src = self.get_image_url()
        return f"Photo({src})" if src else f"Photo(id={self.pk})"
    
    
class Follow(models.Model):
    """Showing a follower in a profile."""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.follower_profile} follows {self.profile}"
    
    
class Comment(models.Model):
    """A response by a Profile on a Post."""
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='comments_made')
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=False)

    def __str__(self):
        who = str(self.profile)    
        return f'{who} on Post #{self.post_id}: {self.text[:40]}'
    

class Like(models.Model):
    """One Profile liking one Post."""
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes')
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='likes_made')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.profile} likes Post #{self.post_id}"