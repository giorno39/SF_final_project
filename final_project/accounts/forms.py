from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.forms import formset_factory

from final_project.accounts.models import TeacherProfile, TypesOfUsers, TeacherSpecializationRequest

UserModel = get_user_model()


class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.setdefault(
            'placeholder', 'Enter your username',
        )
        self.fields['password'].widget.attrs.setdefault(
            'placeholder', 'Enter your password',
        )


class PasswordChangeStyledForm(auth_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.setdefault(
            'placeholder', 'Current password',
        )
        self.fields['new_password1'].widget.attrs.setdefault(
            'placeholder', 'New password',
        )
        self.fields['new_password2'].widget.attrs.setdefault(
            'placeholder', 'Confirm new password',
        )


class UserCreateForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'user_type')
        field_classes = {
            'username': auth_forms.UsernameField,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.setdefault(
            'placeholder', 'Choose a username',
        )
        self.fields['email'].widget.attrs.setdefault(
            'placeholder', 'name@example.com',
        )
        self.fields['user_type'].choices = [
            (TypesOfUsers.student.value, 'Student'),
            (TypesOfUsers.teacher.value, 'Teacher'),
        ]
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.setdefault(
                'placeholder', 'Create a password',
            )
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.setdefault(
                'placeholder', 'Confirm password',
            )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if UserModel.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "A user with this email already exists."
            )

        return email


class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'name@example.com'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')

        qs = UserModel.objects.filter(email__iexact=email)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "This email is already in use by another account."
            )

        return email


class TeacherSpecializationsForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ("specializations",)
        widgets = {
            "specializations": forms.CheckboxSelectMultiple(),
        }

    def clean_specializations(self):
        specs = self.cleaned_data.get("specializations")
        if not specs or specs.count() == 0:
            raise forms.ValidationError("Please select at least one specialization.")
        return specs

class TeacherSpecializationProofForm(forms.ModelForm):
    class Meta:
        model = TeacherSpecializationRequest
        fields = ("proof_file",)
        widgets = {
            "proof_file": forms.ClearableFileInput(attrs={"class": "input"}),
        }


TeacherSpecializationProofFormSet = formset_factory(
    TeacherSpecializationProofForm,
    extra=0,
)