from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Voter
from .forms import VoterFilterForm

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