from django import forms

from django.utils.translation import gettext_lazy as _
from final_project.accounts.models import Specialization
from final_project.useful_materials.models import Materials, MaterialComment
from final_project.useful_materials.services.reference_validation import validate_reference_with_ai


class MaterialCreateForm(forms.ModelForm):
    class Meta:
        model = Materials
        exclude = ('uploaded_by',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('Enter material title…')}),
            'specializations': forms.CheckboxSelectMultiple(),
            'content': forms.ClearableFileInput(attrs={'accept': 'application/pdf,.pdf'}),
            'references': forms.URLInput(attrs={'placeholder': 'https://…'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["specializations"].label_from_instance = (
            lambda obj: obj.translated_name
        )

    def clean(self):
        cleaned_data = super().clean()

        reference_url = cleaned_data.get('references')
        specializations = cleaned_data.get('specializations')

        if reference_url:
            specialization_names = [
                str(spec.translated_name) for spec in specializations
            ] if specializations else []

            validation_result = validate_reference_with_ai(
                reference_url,
                specialization_names,
            )

            if not validation_result.get('is_allowed'):
                self.add_error(
                    'references',
                    validation_result.get('reason', _('This reference is not allowed.'))
                )

        return cleaned_data


class MaterialEditForm(forms.ModelForm):
    class Meta:
        model = Materials
        exclude = ('uploaded_by',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('Enter material title…')}),
            'specializations': forms.CheckboxSelectMultiple(),
            'content': forms.ClearableFileInput(attrs={'accept': 'application/pdf,.pdf'}),
            'references': forms.URLInput(attrs={'placeholder': 'https://…'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["specializations"].label_from_instance = (
            lambda obj: obj.translated_name
        )

    def clean(self):
        cleaned_data = super().clean()

        reference_url = cleaned_data.get('references')
        specializations = cleaned_data.get('specializations')

        if reference_url:
            specialization_names = [
                str(spec.translated_name) for spec in specializations
            ] if specializations else []

            validation_result = validate_reference_with_ai(
                reference_url,
                specialization_names,
            )

            if not validation_result.get('is_allowed'):
                self.add_error(
                    'references',
                    validation_result.get('reason', _('This reference is not allowed.'))
                )

        return cleaned_data


class MaterialSearchForm(forms.Form):
    material_title = forms.CharField(
        max_length=Materials.TITLE_MAX_LEN,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Search by title…"),
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


class MaterialCommentForm(forms.ModelForm):
    class Meta:
        model = MaterialComment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': _('Write your comment here...'),
            }),
        }