from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

from .models import (
    Specialization,
    TeacherProfile,
    StudentProfile,
    TeacherSpecializationRequest,
)
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

    @admin.display(empty_value='-')
    def has_last_name(self, obj):
        return obj.last_name or '-'

    @admin.display(empty_value='-')
    def has_first_name(self, obj):
        return obj.first_name or '-'


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username", "user__email")
    filter_horizontal = ("specializations",)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username", "user__email")


@admin.register(TeacherSpecializationRequest)
class TeacherSpecializationRequestAdmin(admin.ModelAdmin):
    list_display = ("teacher", "specialization", "status", "created_at", "reviewed_at", "reviewed_by")
    list_filter = ("status", "specialization", "created_at")
    search_fields = ("teacher__user__username", "teacher__user__email", "specialization__name")
    autocomplete_fields = ("teacher", "specialization", "reviewed_by")