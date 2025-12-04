from django import forms
from .models import Campaign, Post


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'objective', 'channel', 'start_date', 'end_date', 'budget']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['campaign', 'post_date', 'content_type', 'caption', 'url']
