from django import forms

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
            'price': forms.NumberInput(attrs={'placeholder': '0', 'min': 0}),
            'cover_image': forms.FileInput(
                attrs={'accept': 'image/*', 'class': 'lesson-cover-input'},
            ),
        }


class LessonEditForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'subject', 'price', 'cover_image')
        labels = {
            'cover_image': 'Cover photo (optional)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Lesson title'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject area'}),
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
                'placeholder': 'Search lessons by title, subject, or keyword…',
                'class': 'lesson-feed-search-input',
                'autocomplete': 'off',
            },
        ),
    )
