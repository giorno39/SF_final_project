from django import forms

from final_project.useful_materials.models import Materials


class MaterialCreateForm(forms.ModelForm):
    class Meta:
        model = Materials
        exclude = ('uploaded_by',)
