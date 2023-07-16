from django import forms

from final_project.lessons.models import Lesson


class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        exclude = ('teacher',)
