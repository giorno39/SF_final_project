from django import forms

from final_project.accounts.models import Specialization
from final_project.completed_papers.models import CompletedPaper


class CompletedPaperSearchForm(forms.Form):
    completed_title = forms.CharField(
        max_length=CompletedPaper.TERM_PAPER_MAX_LEN,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search by title...',
                'autocomplete': 'off',
            }
        ),
    )

    specialization = forms.ModelChoiceField(
        queryset=Specialization.objects.all(),
        required=False,
        empty_label='All specializations',
    )