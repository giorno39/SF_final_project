from django import forms

from final_project.useful_materials.models import Materials


class MaterialCreateForm(forms.ModelForm):
    class Meta:
        model = Materials
        exclude = ('uploaded_by',)

class MaterialSearchForm(forms.Form):
    material_title = forms.CharField(
        max_length=Materials.TITLE_MAX_LEN,
        required=False,
    )
