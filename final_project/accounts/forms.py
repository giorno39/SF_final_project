import os

from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.core.exceptions import ValidationError
from django.forms import formset_factory
from django.utils.translation import gettext_lazy as _

from final_project.accounts.models import TeacherProfile, TypesOfUsers, TeacherSpecializationRequest

UserModel = get_user_model()

ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png'}

def validate_proof_file(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            _("Only PDF, JPG, JPEG, and PNG files are allowed.")
        )

class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.setdefault(
            'placeholder', _('Enter your username'),
        )
        self.fields['password'].widget.attrs.setdefault(
            'placeholder', _('Enter your password'),
        )


class PasswordChangeStyledForm(auth_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.setdefault(
            'placeholder', _('Current password'),
        )
        self.fields['new_password1'].widget.attrs.setdefault(
            'placeholder', _('New password'),
        )
        self.fields['new_password2'].widget.attrs.setdefault(
            'placeholder', _('Confirm new password'),
        )


class UserCreateForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'user_type')
        field_classes = {
            'username': auth_forms.UsernameField,
        }
        labels = {
            'username': _('Username'),
            'email': _('Email'),
            'user_type': _('User type'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.setdefault(
            'placeholder', _('Choose a username'),
        )
        self.fields['email'].widget.attrs.setdefault(
            'placeholder', _('name@example.com'),
        )

        self.fields['user_type'].choices = [
            (TypesOfUsers.STUDENT, _('Student')),
            (TypesOfUsers.TEACHER, _('Teacher')),
        ]

        if 'password1' in self.fields:
            self.fields['password1'].label = _('Password')
            self.fields['password1'].widget.attrs.setdefault(
                'placeholder', _('Create a password'),
            )

        if 'password2' in self.fields:
            self.fields['password2'].label = _('Password confirmation')
            self.fields['password2'].widget.attrs.setdefault(
                'placeholder', _('Confirm password'),
            )


class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': _('First name')}),
            'last_name': forms.TextInput(attrs={'placeholder': _('Last name')}),
            'email': forms.EmailInput(attrs={'placeholder': _('name@example.com')}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')

        qs = UserModel.objects.filter(email__iexact=email)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                _("A user with this email already exists.")
            )

        return email


class TeacherSpecializationsForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ("specializations",)
        widgets = {
            "specializations": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["specializations"].label_from_instance = (
            lambda obj: obj.translated_name
        )

    def clean_specializations(self):
        specs = self.cleaned_data.get("specializations")
        if not specs or specs.count() == 0:
            raise forms.ValidationError(
                _("Please select at least one specialization.")
            )
        return specs

class TeacherSpecializationProofForm(forms.ModelForm):
    proof_file = forms.FileField(
        validators=[validate_proof_file],
        widget=forms.FileInput(
            attrs={
                "class": "spec-proof-native-input",
                "accept": ".pdf,.jpg,.jpeg,.png",
            }
        ),
    )

    class Meta:
        model = TeacherSpecializationRequest
        fields = ("proof_file",)


TeacherSpecializationProofFormSet = formset_factory(
    TeacherSpecializationProofForm,
    extra=0,
)