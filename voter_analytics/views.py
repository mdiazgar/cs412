from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Voter
from .forms import VoterFilterForm
from django.db.models import Count, Sum
from django.db.models.functions import ExtractYear
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.io import to_html
from django.utils.http import urlencode

# Create your views here.

class VoterListView(ListView):
    model = Voter
    template_name = "voter_analytics/voter_list.html"
    context_object_name = "voters"
    paginate_by = 100
    ordering = ["last_name", "first_name"]

    def get_queryset(self):
        qs = super().get_queryset()
        self.filter_form = VoterFilterForm(self.request.GET or None)

        if self.filter_form.is_valid():
            cd = self.filter_form.cleaned_data

            if cd.get("party"):
                qs = qs.filter(party=cd["party"])

            if cd.get("min_year"):
                qs = qs.filter(date_birth__year__gte=int(cd["min_year"]))

            if cd.get("max_year"):
                qs = qs.filter(date_birth__year__lte=int(cd["max_year"]))

            if cd.get("voter_score"):
                qs = qs.filter(voter_score=int(cd["voter_score"]))

            for field in cd.get("elections", []):
                qs = qs.filter(**{field: 1})

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = getattr(self, "filter_form", VoterFilterForm())
        return ctx


class VoterDetailView(DetailView):
    model = Voter
    template_name = "voter_analytics/voter_detail.html"
    context_object_name = "voter"
    
    
class VoterGraphsView(ListView):
    """
    Graphs page (reuse ListView per spec). Uses filter form from Task 2 to
    restrict the queryset and then draws Plotly graphs for the filtered set.
    """
    model = Voter
    template_name = "voter_analytics/graphs.html"
    context_object_name = "voters"
    paginate_by = 0  # no table pagination on graphs page

    def get_queryset(self):
        qs = Voter.objects.all()
        g = self.request.GET

        if g.get("party"):
            qs = qs.filter(party=g["party"])

        if g.get("min_year"):
            qs = qs.filter(date_birth__year__gte=int(g["min_year"]))

        if g.get("max_year"):
            qs = qs.filter(date_birth__year__lte=int(g["max_year"]))

        if g.get("score"):
            qs = qs.filter(voter_score=int(g["score"]))

        for f in ("v20state", "v21town", "v21primary", "v22general", "v23town"):
            if g.get(f) == "on":
                qs = qs.filter(**{f: 1})

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = ctx["voters"]
        n = qs.count()

        # ----- choices for filters (reuse Task 2) -----
        ctx["party_choices"] = (
            Voter.objects.exclude(party__isnull=True)
                         .exclude(party__exact="")
                         .values_list("party", flat=True)
                         .distinct()
                         .order_by("party")
        )
        ctx["year_choices"] = (
            Voter.objects.exclude(date_birth__isnull=True)
                         .annotate(y=ExtractYear("date_birth"))
                         .values_list("y", flat=True)
                         .distinct()
                         .order_by("y")
        )
        ctx["score_choices"] = (
            Voter.objects.values_list("voter_score", flat=True)
                         .distinct()
                         .order_by("voter_score")
        )
        ctx["election_filters"] = [
            ("v20state",   "2020 State"),
            ("v21town",    "2021 Town"),
            ("v21primary", "2021 Primary"),
            ("v22general", "2022 General"),
            ("v23town",    "2023 Town"),
        ]
        ctx["checked_elections"] = {
            k for k in self.request.GET.keys()
            if k in {f for f, _ in ctx["election_filters"]}
        }

        # If there are no rows after filtering, show a friendly message and exit early
        if n == 0:
            ctx["birth_hist_html"] = ctx["party_pie_html"] = ctx["elections_bar_html"] = ""
            ctx["empty_msg"] = "No data for the selected filters."
            return ctx

        # ----- Graph 1: Year-of-birth histogram -----
        yob = (
            qs.exclude(date_birth__isnull=True)
              .annotate(y=ExtractYear("date_birth"))
              .values("y")
              .annotate(c=Count("id"))
              .order_by("y")
        )
        years = [row["y"] for row in yob]
        counts = [row["c"] for row in yob]

        fig_birth = go.Figure(data=[go.Bar(x=years, y=counts)])
        fig_birth.update_layout(
            title=f"Voter distribution by Year of Birth (n={n})",
            xaxis_title="Year of birth",
            yaxis_title="Count",
            bargap=0.05,
            margin=dict(l=40, r=20, t=60, b=40),
            height=420,
        )
        ctx["birth_hist_html"] = to_html(fig_birth, full_html=False, include_plotlyjs="cdn")

        # ----- Graph 2: Party affiliation pie -----
        party_rows = (
            qs.values("party")
              .annotate(c=Count("id"))
              .order_by("party")
        )
        party_labels = [ (r["party"] or "Unknown").strip() for r in party_rows ]
        party_values = [ r["c"] for r in party_rows ]

        fig_party = go.Figure(data=[go.Pie(labels=party_labels, values=party_values, hole=0)])
        fig_party.update_layout(
            title=f"Voter distribution by Party Affiliation (n={n})",
            margin=dict(l=40, r=20, t=60, b=40),
            height=420,
        )
        ctx["party_pie_html"] = to_html(fig_party, full_html=False, include_plotlyjs=False)

        # ----- Graph 3: Vote count by election (bar) -----
        agg = qs.aggregate(
            v20state=Sum("v20state"),
            v21town=Sum("v21town"),
            v21primary=Sum("v21primary"),
            v22general=Sum("v22general"),
            v23town=Sum("v23town"),
        )
        vote_labels = ["v20state", "v21town", "v21primary", "v22general", "v23town"]
        vote_values = [int(agg[k] or 0) for k in vote_labels]

        fig_votes = go.Figure(data=[go.Bar(x=vote_labels, y=vote_values)])
        fig_votes.update_layout(
            title=f"Vote Count by Election (n={n})",
            xaxis_title="Election",
            yaxis_title="Count voted (1=Yes)",
            margin=dict(l=40, r=20, t=60, b=40),
            height=420,
        )
        ctx["elections_bar_html"] = to_html(fig_votes, full_html=False, include_plotlyjs=False)

        return ctx