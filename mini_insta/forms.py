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
       

