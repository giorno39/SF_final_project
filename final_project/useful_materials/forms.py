from django import forms

from final_project.accounts.models import Specialization
from final_project.useful_materials.models import Materials, MaterialComment


class MaterialCreateForm(forms.ModelForm):
    class Meta:
        model = Materials
        exclude = ('uploaded_by',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter material title…'}),
            'specializations': forms.CheckboxSelectMultiple(),
            'content': forms.ClearableFileInput(attrs={'accept': 'application/pdf,.pdf'}),
            'references': forms.URLInput(attrs={'placeholder': 'https://…'}),
        }


class MaterialEditForm(forms.ModelForm):
    class Meta:
        model = Materials
        exclude = ('uploaded_by',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter material title…'}),
            'specializations': forms.CheckboxSelectMultiple(),
            'content': forms.ClearableFileInput(attrs={'accept': 'application/pdf,.pdf'}),
            'references': forms.URLInput(attrs={'placeholder': 'https://…'}),
        }


class MaterialSearchForm(forms.Form):
    material_title = forms.CharField(
        max_length=Materials.TITLE_MAX_LEN,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by title…'}),
    )

    specialization = forms.ModelChoiceField(
        queryset=Specialization.objects.all(),
        required=False,
        empty_label='All specializations',
    )


class MaterialCommentForm(forms.ModelForm):
    class Meta:
        model = MaterialComment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your comment here...',
            }),
        }