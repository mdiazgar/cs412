from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Channel, Campaign, Post
from .forms import CampaignForm, PostForm
from django.shortcuts import render
from django.db.models import Sum
from datetime import datetime


class ChannelListView(LoginRequiredMixin, ListView):
    model = Channel
    template_name = 'project/channel_list.html'
    context_object_name = 'channels'

    def get_queryset(self):
        return Channel.objects.filter(owner=self.request.user)


class ChannelDetailView(LoginRequiredMixin, DetailView):
    model = Channel
    template_name = 'project/channel_detail.html'
    context_object_name = 'channel'

    def get_queryset(self):
        # así nadie puede ver canales de otros usuarios si adivina el ID
        return Channel.objects.filter(owner=self.request.user)


class CampaignListView(LoginRequiredMixin, ListView):
    model = Campaign
    template_name = 'project/campaign_list.html'
    context_object_name = 'campaigns'

    def get_queryset(self):
        return (
            Campaign.objects
            .filter(channel__owner=self.request.user)
            .select_related('channel')
        )


class CampaignDetailView(LoginRequiredMixin, DetailView):
    model = Campaign
    template_name = 'project/campaign_detail.html'
    context_object_name = 'campaign'

    def get_queryset(self):
        return (
            Campaign.objects
            .filter(channel__owner=self.request.user)
            .select_related('channel')
        )


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'project/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return (
            Post.objects
            .filter(campaign__channel__owner=self.request.user)
            .select_related('campaign')
        )



class CampaignCreateView(LoginRequiredMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'project/campaign_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['channel'].queryset = Channel.objects.filter(owner=self.request.user)
        return form

    def get_success_url(self):
        return reverse_lazy('project:campaign_detail', kwargs={'pk': self.object.pk})


class CampaignUpdateView(LoginRequiredMixin, UpdateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'project/campaign_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['channel'].queryset = Channel.objects.filter(owner=self.request.user)
        return form

    def get_queryset(self):
        return Campaign.objects.filter(channel__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('project:campaign_detail', kwargs={'pk': self.object.pk})



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'project/post_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['campaign'].queryset = Campaign.objects.filter(
            channel__owner=self.request.user
        )
        return form

    def get_success_url(self):
        return reverse_lazy('project:post_detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return Post.objects.filter(campaign__channel__owner=self.request.user)

    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'project/post_confirm_delete.html'

    def get_queryset(self):
        return Post.objects.filter(campaign__channel__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            'project:campaign_detail',
            kwargs={'pk': self.object.campaign.pk}
        )


@login_required
def campaign_performance_report(request):
    channel_id = request.GET.get('channel')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    campaigns = (
        Campaign.objects
        .filter(channel__owner=request.user)
        .select_related('channel')
    )

    if channel_id:
        campaigns = campaigns.filter(channel_id=channel_id)

    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            campaigns = campaigns.filter(start_date__gte=start_date)
        except ValueError:
            start_date = None
    else:
        start_date = None

    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            campaigns = campaigns.filter(start_date__lte=end_date)
        except ValueError:
            end_date = None
    else:
        end_date = None

    results = []
    for campaign in campaigns:
        posts = campaign.posts.all().select_related('metrics')

        total_impressions = 0
        total_likes = 0
        total_comments = 0
        total_shares = 0
        total_clicks = 0

        for post in posts:
            if hasattr(post, 'metrics') and post.metrics:
                total_impressions += post.metrics.impressions
                total_likes += post.metrics.likes
                total_comments += post.metrics.comments
                total_shares += post.metrics.shares
                total_clicks += post.metrics.clicks

        if total_impressions > 0:
            engagement_rate = (total_likes + total_comments + total_shares) / total_impressions
            ctr = total_clicks / total_impressions
        else:
            engagement_rate = 0
            ctr = 0

        results.append({
            'campaign': campaign,
            'total_impressions': total_impressions,
            'total_likes': total_likes,
            'total_comments': total_comments,
            'total_shares': total_shares,
            'total_clicks': total_clicks,
            'engagement_rate': engagement_rate,
            'ctr': ctr,
        })

    results.sort(key=lambda x: x['total_impressions'], reverse=True)

    channels = Channel.objects.filter(owner=request.user)

    context = {
        'channels': channels,
        'results': results,
        'selected_channel_id': channel_id or '',
        'start_date': start_date_str or '',
        'end_date': end_date_str or '',
    }
    return render(request, 'project/report_campaign_performance.html', context)
