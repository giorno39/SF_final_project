from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

from final_project.accounts.models import AppUser
from final_project.completed_papers.models import CompletedPaper
from final_project.lessons.models import Lesson
from final_project.term_papers.models import TermPaper
from final_project.trophies.models import Trophy

UserModel = get_user_model()


class AdminUserCreateForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        exclude = ('password',)
        field_classes = {
            'username': auth_forms.UsernameField,
        }


class AdminLessonCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = AppUser.objects.filter(user_type='teacher')

    class Meta:
        model = Lesson
        fields = '__all__'


class AdminTermPaperCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = AppUser.objects.filter(user_type='student')
        self.fields['taken_by'].queryset = AppUser.objects.filter(user_type='teacher')

    class Meta:
        model = TermPaper
        fields = '__all__'


class AdminCompletedPaperCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['completed_by'].queryset = AppUser.objects.filter(user_type='teacher')

    class Meta:
        model = CompletedPaper
        fields = '__all__'


class AdminTrophyCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['completed_by'].queryset = AppUser.objects.filter(user_type='teacher')

    class Meta:
        model = Trophy
        fields = '__all__'
