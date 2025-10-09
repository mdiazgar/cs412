# File: mini_insta/models.py
# Author: María Díaz Garrido
# Description: Database models for the mini_insta app. Defines the Profile model
#              with username, display_name, bio_text, profile_image_url (URL),
#              and join_date (auto-updated). __str__ returns the username.


from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    "Encapsulate the data of a mini insta"
    
    #define the data attributes of the Mini_insta object
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