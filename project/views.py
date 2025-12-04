from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Channel, Campaign, Post
from .forms import CampaignForm, PostForm


class ChannelListView(ListView):
    model = Channel
    template_name = 'project/channel_list.html'
    context_object_name = 'channels'


class ChannelDetailView(DetailView):
    model = Channel
    template_name = 'project/channel_detail.html'
    context_object_name = 'channel'


class CampaignListView(ListView):
    model = Campaign
    template_name = 'project/campaign_list.html'
    context_object_name = 'campaigns'


class CampaignDetailView(DetailView):
    model = Campaign
    template_name = 'project/campaign_detail.html'
    context_object_name = 'campaign'


class PostDetailView(DetailView):
    model = Post
    template_name = 'project/post_detail.html'
    context_object_name = 'post'


class CampaignCreateView(CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'project/campaign_form.html'

    def get_success_url(self):
        return reverse_lazy('project:campaign_detail', kwargs={'pk': self.object.pk})


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'project/post_form.html'

    def get_success_url(self):
        return reverse_lazy('project:post_detail', kwargs={'pk': self.object.pk})
