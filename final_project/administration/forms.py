from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

from final_project.accounts.models import AppUser
from final_project.completed_papers.models import CompletedPaper
from final_project.lessons.models import Lesson
from final_project.term_papers.models import TermPaper
from final_project.trophies.models import Trophy

UserModel = get_user_model()


def apply_input_placeholders(form):
    """Set placeholder on text-like widgets when not already set."""
    for name, field in form.fields.items():
        w = field.widget
        if isinstance(w, (forms.TextInput, forms.EmailInput, forms.URLInput)):
            if 'placeholder' not in w.attrs:
                label = field.label or name.replace('_', ' ').title()
                w.attrs['placeholder'] = f'Enter {label}'
        elif isinstance(w, forms.NumberInput):
            if 'placeholder' not in w.attrs:
                w.attrs['placeholder'] = field.label or '0'
        elif isinstance(w, forms.PasswordInput):
            if 'placeholder' not in w.attrs:
                label = field.label or name.replace('_', ' ').title()
                w.attrs['placeholder'] = label
        elif isinstance(w, forms.Textarea):
            if 'placeholder' not in w.attrs and field.label:
                w.attrs['placeholder'] = field.label


class AdminUserCreateForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        exclude = ('password',)
        field_classes = {
            'username': auth_forms.UsernameField,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_input_placeholders(self)


class AdminLessonCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = AppUser.objects.filter(user_type='teacher')
        apply_input_placeholders(self)

    class Meta:
        model = Lesson
        fields = '__all__'


class AdminTermPaperCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = AppUser.objects.filter(user_type='student')
        self.fields['taken_by'].queryset = AppUser.objects.filter(user_type='teacher')
        apply_input_placeholders(self)

    class Meta:
        model = TermPaper
        fields = '__all__'


class AdminCompletedPaperCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['completed_by'].queryset = AppUser.objects.filter(user_type='teacher')
        apply_input_placeholders(self)

    class Meta:
        model = CompletedPaper
        fields = '__all__'


class AdminTrophyCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['completed_by'].queryset = AppUser.objects.filter(user_type='teacher')
        apply_input_placeholders(self)

    class Meta:
        model = Trophy
        fields = '__all__'
