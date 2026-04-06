from django import forms

from final_project.accounts.models import Specialization
from final_project.lessons.models import Lesson


class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        exclude = ('teacher',)
        labels = {
            'cover_image': 'Cover photo (optional)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Lesson title'}),
            'subject': forms.TextInput(attrs={'placeholder': 'e.g., Mathematics, Science…'}),
            'specializations': forms.CheckboxSelectMultiple(),
            'price': forms.NumberInput(attrs={'placeholder': '0', 'min': 0}),
            'cover_image': forms.FileInput(
                attrs={'accept': 'image/*', 'class': 'lesson-cover-input'},
            ),
        }


class LessonEditForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'specializations', 'price', 'cover_image')
        labels = {
            'cover_image': 'Cover photo (optional)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Lesson title'}),
            'specializations': forms.CheckboxSelectMultiple(),
            'price': forms.NumberInput(attrs={'placeholder': '0', 'min': 0}),
            'cover_image': forms.FileInput(
                attrs={'accept': 'image/*', 'class': 'lesson-cover-input'},
            ),
        }


class LessonSearchForm(forms.Form):
    lesson_title = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search by title...',
                'autocomplete': 'off',
            },
        ),
    )

    specialization = forms.ModelChoiceField(
        queryset=Specialization.objects.all(),
        required=False,
        empty_label='All specializations',
    )