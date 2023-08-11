from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

from final_project.accounts.forms import UserEditForm, UserCreateForm

UserModel = get_user_model()


@admin.register(UserModel)
class UserAdmin(auth_admin.UserAdmin):
    form = UserEditForm
    add_form = UserCreateForm
    list_display = ['username', 'email', 'has_first_name', 'has_last_name', 'user_type']
    ordering = ['-date_joined', ]
    list_filter = ['user_type', 'is_staff', 'is_superuser']
    list_display_links = ['username', 'email']

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'password',
                ),
            }),
        (
            'Personal info',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'user_type'
                ),
            },
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                ),
            },
        ),
        (
            'Important dates',
            {
                'fields': (
                    'last_login',
                    'date_joined',
                ),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        return super().get_form(request, obj, **kwargs)

    @admin.display(empty_value='-')
    def has_last_name(self, obj):
        if not obj.last_name:
            return '-'
        return obj.last_name

    has_last_name.short_description = 'LAST NAME'
    has_last_name.admin_order_field = 'last_name'

    @admin.display(empty_value='-')
    def has_first_name(self, obj):
        if not obj.first_name:
            return '-'
        return obj.first_name

    has_first_name.short_description = 'FIRST NAME'
    has_first_name.admin_order_field = 'first_name'
