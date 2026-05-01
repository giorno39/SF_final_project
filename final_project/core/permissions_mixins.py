from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from final_project.accounts.models import TypesOfUsers


class TeacherRequiredMixin(LoginRequiredMixin):
    login_url = "login-user"   # replace if your url name is different

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.user_type != TypesOfUsers.TEACHER:
            return render(request, "common/no-perms.html")

        return super().dispatch(request, *args, **kwargs)

class ReviewerRequiredMixin(LoginRequiredMixin):
    login_url = "login-user"  # set your actual login url name if needed

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not (
            request.user.is_staff
            or request.user.user_type == TypesOfUsers.REVIEWER
        ):
            return render(request, "common/no-perms.html")

        return super().dispatch(request, *args, **kwargs)


class StudentRequiredMixin(LoginRequiredMixin):
    login_url = "login-user"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.user_type != TypesOfUsers.STUDENT:
            return render(request, "common/no-perms.html")

        return super().dispatch(request, *args, **kwargs)