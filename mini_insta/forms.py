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
        

