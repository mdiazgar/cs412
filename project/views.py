"""
views.py

Views for the Campaign Analytics application.

Provides:
- Dashboard and listing views for channels and campaigns.
- CRUD views for channels, campaigns, posts and objectives.
- A campaign performance report with filtering and aggregated metrics.
- Authentication-protected access using Django's login_required.
"""

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Channel, Campaign, Post
from .forms import CampaignForm, PostForm
from django.shortcuts import render
from django.db.models import Sum
from datetime import datetime
import json
from django.utils.safestring import mark_safe


class ChannelListView(LoginRequiredMixin, ListView):
    """
    List all social media channels that belong to the logged-in user.

    This is the main dashboard entry point and only shows channels owned
    by the current user, so different users never see each other's data.
    """
    model = Channel
    template_name = 'project/channel_list.html'
    context_object_name = 'channels'

    def get_queryset(self):
        return Channel.objects.filter(owner=self.request.user)


class ChannelDetailView(LoginRequiredMixin, DetailView):
    """
    Display details for a single Channel owned by the current user.

    The template can show channel metadata and link to the campaigns
    running on this channel. Access is restricted by owner.
    """
    model = Channel
    template_name = 'project/channel_detail.html'
    context_object_name = 'channel'

    def get_queryset(self):
        return Channel.objects.filter(owner=self.request.user)


class CampaignListView(LoginRequiredMixin, ListView):
    """
    List all campaigns that belong to the current user.

    Shows basic campaign information grouped by channel and provides
    links to view details, edit, or delete a campaign.
    """
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
    """
    Display the detail page for a single Campaign.
    - Restricts access to campaigns that belong to the current user
      (via the channel.owner relationship).
    - Retrieves all posts in the campaign and prepares time-series data
      (impressions, clicks and engagement rate) to be rendered as a
      Chart.js visual summary in the template.
    """
    model = Campaign
    template_name = 'project/campaign_detail.html'

    def get_queryset(self):
        return (
            Campaign.objects
            .filter(channel__owner=self.request.user)
            .select_related('channel')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign = self.object

        posts = (
            campaign.posts
            .order_by('post_date')
            .select_related('metrics')
        )

        labels = []
        impressions = []
        clicks = []
        engagement = []

        for post in posts:
            if post.post_date:
                label = post.post_date.strftime('%b %d')
            else:
                label = f"Post {post.id}"

            labels.append(label)

            if hasattr(post, 'metrics') and post.metrics:
                m = post.metrics
                impressions.append(m.impressions)
                clicks.append(m.clicks)
                if m.impressions > 0:
                    er = (m.likes + m.comments + m.shares) / m.impressions
                else:
                    er = 0
                engagement.append(round(er, 3))
            else:
                impressions.append(0)
                clicks.append(0)
                engagement.append(0)

        context['chart_labels'] = mark_safe(json.dumps(labels))
        context['chart_impressions'] = mark_safe(json.dumps(impressions))
        context['chart_clicks'] = mark_safe(json.dumps(clicks))
        context['chart_engagement'] = mark_safe(json.dumps(engagement))

        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    """
    Display the details of a single Post that belongs to the current user.

    The view shows basic post info (date, caption, URL) and its metrics.
    Access is restricted so that a user can only see posts whose campaign
    is attached to one of their own channels.
    """
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
    """
    Allow the user to create a new campaign.

    Uses CampaignForm to validate input, automatically associates the
    campaign with the selected channel, and redirects to the campaign
    list on success.
    """
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
    """
    Allow the user to edit an existing campaign.

    Reuses CampaignForm and enforces that only campaigns belonging to
    the current user's channels can be updated.
    """
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
    """
    Create a new Post for one of the user's campaigns.

    Once the post is created, an empty PostMetrics record may also be
    created (if you do this in form_valid) so that performance data can
    be added later.
    """
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
    """
    Delete a Post for one of the user's campaigns.

    """
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
    """
    Render an aggregated performance report across campaigns.

    The view accepts optional GET parameters:
    - channel: filter campaigns by channel id.
    - start_date, end_date: filter campaigns whose date range overlaps
      with the selected period.

    For each campaign, it sums post metrics (impressions, likes,
    comments, shares, clicks) and computes engagement rate and CTR.
    Results are passed to the 'project/report_campaign_performance.html'
    template sorted by total impressions.
    """
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
