from django import forms

from final_project.term_papers.models import TermPaper


class TermPaperCreateForm(forms.ModelForm):
    class Meta:
        model = TermPaper
        fields = ('title', 'subject', 'university', 'death_line', 'price_cap', 'description', 'content')

        widgets = {
            'death_line': forms.SelectDateWidget(
                attrs={
                    'placeholder': 'death_line',
                       }
            )
        }


class TermPaperSearchForm(forms.Form):
    paper_title = forms.CharField(
        max_length=TermPaper.TERM_PAPER_MAX_LEN,
        required=False,
    )
