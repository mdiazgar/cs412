# File: mini_insta/models.py
# Author: María Díaz Garrido
# Description: Database models for the mini_insta app. Defines the Profile model
#              with username, display_name, bio_text, profile_image_url (URL),
#              and join_date (auto-updated). __str__ returns the username.


from django.db import models

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