"""
forms.py

Model forms for the Campaign Analytics application, used to create and
edit channels, campaigns and posts with Bootstrap-friendly widgets.
"""
from django import forms
from .models import Campaign, Post


class CampaignForm(forms.ModelForm):
    """
    Form used to create or update Campaign instances.

    Customises widgets for date and budget fields so they integrate
    with the dark-mode Bootstrap theme used in the UI.
    """
    class Meta:
        model = Campaign
        fields = ['name', 'objective', 'channel', 'start_date', 'end_date', 'budget']


class PostForm(forms.ModelForm):
    """
    Form used to create or update Post instances.

    Customises widgets for date and budget fields so they integrate
    with the dark-mode Bootstrap theme used in the UI.
    """
    class Meta:
        model = Post
        fields = ['campaign', 'post_date', 'content_type', 'caption', 'url']
