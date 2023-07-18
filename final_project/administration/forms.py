
from django.contrib.auth import forms as auth_forms, get_user_model

UserModel = get_user_model()

class AdminUserCreateForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        exclude = ('password',)
        field_classes = {
            'username': auth_forms.UsernameField,
        }
