from django import forms

from final_project.lessons.models import Lesson


class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        exclude = ('teacher',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Lesson title'}),
            'subject': forms.TextInput(attrs={'placeholder': 'e.g., Mathematics, Science…'}),
            'price': forms.NumberInput(attrs={'placeholder': '0', 'min': 0}),
        }


class LessonSearchForm(forms.Form):
    lesson_title = forms.CharField(
        max_length=Lesson.TITLE_MAX_LEN,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search lessons by title…'}),
    )
