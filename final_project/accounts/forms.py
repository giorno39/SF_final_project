from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

UserModel = get_user_model()


class UserCreateForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'user_type')
        field_classes = {
            'username': auth_forms.UsernameField,
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if UserModel.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "A user with this email already exists."
            )

        return email


class UserEditForm(auth_forms.UserChangeForm):
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        qs = UserModel.objects.filter(email__iexact=email)

        # exclude the current user
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "This email is already in use by another account."
            )

        return email
