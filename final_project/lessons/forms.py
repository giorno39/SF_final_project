from django import forms

from final_project.lessons.models import Lesson


class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        exclude = ('teacher',)


class LessonSearchForm(forms.Form):
    lesson_title = forms.CharField(
        max_length=Lesson.TITLE_MAX_LEN,
        required=False,
    )
