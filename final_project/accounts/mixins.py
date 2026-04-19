from django.shortcuts import redirect
from django.contrib import messages

from final_project.accounts.models import TypesOfUsers


class ReviewerOrAdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login-user")

        is_reviewer = request.user.user_type == TypesOfUsers.reviewer.value
        is_real_admin = request.user.is_staff or request.user.is_superuser

        if not (is_reviewer or is_real_admin):
            messages.error(request, "You do not have permission to access this page.")
            return redirect("index")

        return super().dispatch(request, *args, **kwargs)