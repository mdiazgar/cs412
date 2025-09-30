from django import forms
from .models import Post
from .models import Photo

# class CreateArticleForm(forms.ModelForm):
#     '''A form to add a picture to the database'''
    
#     class Meta:
#         '''Associate this form with a model from our database'''
#         model = Article
#         fields = ['author', 'title', 'text', 'image_url']
        
# class CreateCommentForm(form.ModelForm):
#     '''A form to add a Comment about an Article'''
    
#     class Meta:
#         '''associate this form with a model from our database'''
#         model = Comment
#         fields = ['article', 'author', 'text']
        
