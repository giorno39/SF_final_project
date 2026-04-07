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
            'specializations': forms.CheckboxSelectMultiple(),
            'price': forms.NumberInput(attrs={'placeholder': '0', 'min': 0}),
            'cover_image': forms.FileInput(
                attrs={'accept': 'image/*', 'class': 'lesson-cover-input'},
            ),
        }

    def clean_specializations(self):
        specializations = self.cleaned_data.get('specializations')
        teacher = getattr(self.instance, 'teacher', None)

        if not specializations:
            return specializations

        if not teacher:
            return specializations

        teacher_profile = getattr(teacher, 'teacher_profile', None)
        if not teacher_profile:
            raise forms.ValidationError(
                'You need a teacher profile with selected specializations before creating lessons.'
            )

        teacher_specialization_ids = set(
            teacher_profile.specializations.values_list('id', flat=True)
        )

        invalid_specializations = [
            spec.name for spec in specializations
            if spec.id not in teacher_specialization_ids
        ]

        if invalid_specializations:
            raise forms.ValidationError(
                'You can only select specializations from your teacher profile. '
                f'Invalid selections: {", ".join(invalid_specializations)}.'
            )

        return specializations


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

    def clean_specializations(self):
        specializations = self.cleaned_data.get('specializations')
        teacher = getattr(self.instance, 'teacher', None)

        if not specializations:
            return specializations

        if not teacher:
            return specializations

        teacher_profile = getattr(teacher, 'teacher_profile', None)
        if not teacher_profile:
            raise forms.ValidationError(
                'You need a teacher profile with selected specializations before editing lessons.'
            )

        teacher_specialization_ids = set(
            teacher_profile.specializations.values_list('id', flat=True)
        )

        invalid_specializations = [
            spec.name for spec in specializations
            if spec.id not in teacher_specialization_ids
        ]

        if invalid_specializations:
            raise forms.ValidationError(
                'You can only select specializations from your teacher profile. '
                f'Invalid selections: {", ".join(invalid_specializations)}.'
            )

        return specializations


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
