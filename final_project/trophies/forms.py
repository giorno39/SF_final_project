from django import forms
from django.utils.translation import gettext_lazy as _

from final_project.trophies.models import Trophy


class TrophySearchForm(forms.Form):
    trophy_owner = forms.IntegerField(
        label=_('Teacher user ID'),
        widget=forms.NumberInput(attrs={
            'placeholder': _('Teacher user ID'),
        }),
    )
