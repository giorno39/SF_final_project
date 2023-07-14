from django import forms

from final_project.term_papers.models import TermPaper


class TermPaperCreateForm(forms.ModelForm):
    class Meta:
        model = TermPaper
        fields = ('title', 'subject', 'university', 'death_line', 'price_cap', 'description', 'content')
