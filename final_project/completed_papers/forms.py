from django import forms

from final_project.completed_papers.models import CompletedPaper


class CompletedPaperSearchForm(forms.Form):
    completed_title = forms.CharField(
        max_length=CompletedPaper.TERM_PAPER_MAX_LEN,
        required=False,
    )
