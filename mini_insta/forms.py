from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to add a picture to the database'''
    image_url = forms.URLField(required=False, label="Image URL")
    image_file = forms.ImageField(required=False)
    
    class Meta:
        '''Associate this form with a model from our database'''
        model = Post
        fields = ['caption']
        
        
class UpdateProfileForm(forms.ModelForm):
    '''A form to update the profile'''
    class Meta:
        model = Profile
        exclude = ("username", "join_date")
       
       
class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["username", "display_name", "bio_text", "profile_image_url"]
        labels = {
            "username": "Handle (profile username)",
            "display_name": "Display name",
            "bio_text": "Bio",
            "profile_image_url": "Image URL",
        }
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "@handle"}),
            "display_name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "bio_text": forms.Textarea(attrs={"rows": 4, "placeholder": "Tell us about you…"}),
            "profile_image_url": forms.URLInput(attrs={"placeholder": "https://..."}),
        }

