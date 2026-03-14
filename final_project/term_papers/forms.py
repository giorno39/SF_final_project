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
            'death_line': forms.SelectDateWidget(
                attrs={
                    'placeholder': 'death_line',
                }
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
    )
