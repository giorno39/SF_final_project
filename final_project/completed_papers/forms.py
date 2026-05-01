from django import forms
from django.utils.translation import gettext_lazy as _

from final_project.accounts.models import Specialization
from final_project.completed_papers.models import CompletedPaper


class CompletedPaperSearchForm(forms.Form):
    completed_title = forms.CharField(
        max_length=CompletedPaper.TERM_PAPER_MAX_LEN,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Search by title..."),
                "autocomplete": "off",
            }
        ),
    )

    specialization = forms.ModelChoiceField(
        queryset=Specialization.objects.all(),
        required=False,
        empty_label=_("All specializations"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["specialization"].label_from_instance = (
            lambda obj: obj.translated_name
        )