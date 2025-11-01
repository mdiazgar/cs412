# voter_analytics/forms.py
# voter_analytics/forms.py
from django import forms
from .models import Voter
from django.db.models import Min, Max

ELECTION_CHOICES = [
    ("v20state", "2020 State"),
    ("v21town", "2021 Town"),
    ("v21primary", "2021 Primary"),
    ("v22general", "2022 General"),
    ("v23town", "2023 Town"),
]

class VoterFilterForm(forms.Form):
    party = forms.ChoiceField(required=False)
    min_year = forms.ChoiceField(required=False)
    max_year = forms.ChoiceField(required=False)
    voter_score = forms.ChoiceField(required=False)
    elections = forms.MultipleChoiceField(
        required=False, choices=ELECTION_CHOICES, widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        parties = (
            Voter.objects.exclude(party__isnull=True)
            .exclude(party__exact="")
            .values_list("party", flat=True)
            .distinct()
            .order_by("party")
        )
        self.fields["party"].choices = [("", "Any")] + [(p, p) for p in parties]

        bounds = Voter.objects.aggregate(lo=Min("date_birth"), hi=Max("date_birth"))
        years = []
        if bounds["lo"] and bounds["hi"]:
            years = list(range(bounds["hi"].year, bounds["lo"].year - 1, -1))
        year_choices = [("", "Any")] + [(str(y), str(y)) for y in years]
        self.fields["min_year"].choices = year_choices
        self.fields["max_year"].choices = year_choices

        scores = (
            Voter.objects.values_list("voter_score", flat=True)
            .distinct()
            .order_by("voter_score")
        )
        self.fields["voter_score"].choices = [("", "Any")] + [
            (str(s), str(s)) for s in scores
        ]

