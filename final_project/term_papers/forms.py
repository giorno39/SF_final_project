from datetime import date

from django import forms
from django.utils.translation import gettext_lazy as _
from final_project.accounts.models import Specialization
from final_project.term_papers.models import TermPaper


class TermPaperCreateForm(forms.ModelForm):
    class Meta:
        model = TermPaper
        fields = (
            "title",
            "specializations",
            "university",
            "death_line",
            "price_cap",
            "description",
            "content",
        )

        labels = {
            "title": _("Title"),
            "specializations": _("Specializations"),
            "university": _("University"),
            "death_line": _("Deadline"),
            "price_cap": _("Price cap"),
            "description": _("Description"),
            "content": _("Content"),
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": _("Term paper title"),
            }),
            "university": forms.TextInput(attrs={
                "placeholder": _("University or institution"),
            }),
            "price_cap": forms.NumberInput(attrs={
                "placeholder": _("Maximum budget (e.g. 100)"),
                "min": 0,
            }),
            "death_line": forms.DateInput(
                attrs={
                    "type": "date",
                },
                format="%Y-%m-%d",
            ),
            "description": forms.Textarea(attrs={
                "placeholder": _("Describe what you need..."),
                "rows": 5,
            }),
            "specializations": forms.CheckboxSelectMultiple(),
            "content": forms.FileInput(attrs={
                "accept": "application/pdf,.pdf",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["specializations"].label_from_instance = (
            lambda obj: obj.translated_name
        )


from django import forms
from django.utils.translation import gettext_lazy as _

class TermPaperSearchForm(forms.Form):
    paper_title = forms.CharField(
        max_length=TermPaper.TERM_PAPER_MAX_LEN,
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

class TermPaperEditForm(forms.ModelForm):
    class Meta:
        model = TermPaper
        fields = (
            "title",
            "death_line",
            "price_cap",
            "description",
        )

        labels = {
            "title": _("Title"),
            "death_line": _("Deadline"),
            "price_cap": _("Price cap"),
            "description": _("Description"),
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": _("Term paper title"),
            }),
            "death_line": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            ),
            "price_cap": forms.NumberInput(attrs={
                "placeholder": _("Maximum budget (e.g. 100)"),
                "min": 0,
            }),
            "description": forms.Textarea(attrs={
                "placeholder": _("Describe what you need..."),
                "rows": 5,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["death_line"].input_formats = ["%Y-%m-%d"]

        if self.instance and self.instance.pk and self.instance.death_line:
            self.initial["death_line"] = self.instance.death_line.strftime("%Y-%m-%d")