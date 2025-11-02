# voter_analytics/forms.py
# voter_analytics/forms.py
from django import forms
from .models import Voter
from django.db.models import Min, Max

class VoterFilterForm(forms.Form):
    def __init__(self, *args, party_choices=None, year_choices=None, score_choices=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["party"] = forms.ChoiceField(
            choices=[("", "Any")] + [(p, p) for p in party_choices or []],
            required=False,
            label="Party"
        )
        self.fields["min_year"] = forms.ChoiceField(
            choices=[("", "Any")] + [(y, y) for y in year_choices or []],
            required=False,
            label="Min birth year"
        )
        self.fields["max_year"] = forms.ChoiceField(
            choices=[("", "Any")] + [(y, y) for y in year_choices or []],
            required=False,
            label="Max birth year"
        )
        self.fields["voter_score"] = forms.ChoiceField(
            choices=[("", "Any")] + [(str(s), str(s)) for s in score_choices or []],
            required=False,
            label="Voter score"
        )

        # Election checkboxes (if checked, require voted=1)
        self.fields["v20state"]    = forms.BooleanField(required=False, label="2020 State")
        self.fields["v21town"]     = forms.BooleanField(required=False, label="2021 Town")
        self.fields["v21primary"]  = forms.BooleanField(required=False, label="2021 Primary")
        self.fields["v22general"]  = forms.BooleanField(required=False, label="2022 General")
        self.fields["v23town"]     = forms.BooleanField(required=False, label="2023 Town")