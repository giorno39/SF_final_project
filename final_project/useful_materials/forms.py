from django import forms

from final_project.useful_materials.models import Materials


class MaterialCreateForm(forms.ModelForm):
    class Meta:
        model = Materials
        exclude = ('uploaded_by',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter material title…'}),
            'field': forms.TextInput(attrs={'placeholder': 'e.g., Mathematics, Science…'}),
            'references': forms.URLInput(attrs={'placeholder': 'https://…'}),
        }


class MaterialSearchForm(forms.Form):
    material_title = forms.CharField(
        max_length=Materials.TITLE_MAX_LEN,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by title…'}),
    )
