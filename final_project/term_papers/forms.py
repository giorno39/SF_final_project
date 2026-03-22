from datetime import date

from django import forms

from final_project.term_papers.models import TermPaper


class TermPaperCreateForm(forms.ModelForm):
    class Meta:
        model = TermPaper
        fields = (
            'title',
            'specializations',
            'university',
            'death_line',
            'price_cap',
            'description',
            'content',
        )

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Term paper title'}),
            'university': forms.TextInput(attrs={'placeholder': 'University or institution'}),
            'price_cap': forms.NumberInput(attrs={'placeholder': 'Maximum budget (e.g. 100)', 'min': 0}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe what you need…', 'rows': 4}),
            'death_line': forms.SelectDateWidget(
                years=range(date.today().year, date.today().year + 8),
                empty_label=('Year', 'Month', 'Day'),
            ),
            'specializations': forms.CheckboxSelectMultiple(),
        }

    def clean_specializations(self):
        specs = self.cleaned_data.get("specializations")
        if not specs or specs.count() == 0:
            raise forms.ValidationError("Please select at least one specialization.")
        return specs


class TermPaperSearchForm(forms.Form):
    paper_title = forms.CharField(
        max_length=TermPaper.TERM_PAPER_MAX_LEN,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search term papers…'}),
    )
