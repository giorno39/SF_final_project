from django import forms

from final_project.trophies.models import Trophy


class TrophySearchForm(forms.Form):
    trophy_owner = forms.IntegerField()
