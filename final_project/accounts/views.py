from statistics import mean

from django.contrib.auth import views as auth_views, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.checks import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from final_project.accounts.forms import (
    LoginForm,
    PasswordChangeStyledForm,
    UserCreateForm,
    UserEditForm,
    TeacherSpecializationsForm,
)
from django.contrib import messages

from final_project.accounts.models import TypesOfUsers, TeacherProfile
from final_project.trophies.models import Trophy

UserModel = get_user_model()


class SignInView(auth_views.LoginView):
    template_name = 'accounts/profile-login.html'
    authentication_form = LoginForm


class SignUpView(views.CreateView):
    model = UserModel
    form_class = UserCreateForm
    template_name = 'accounts/profile-register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)  # creates self.object
        login(self.request, self.object)

        # If teacher -> redirect to onboarding page for specializations
        if self.object.user_type == TypesOfUsers.teacher.value:
            return redirect('teacher-specializations')

        return response


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('index')


class ChangePasswordView(auth_views.PasswordChangeView):
    success_url = reverse_lazy('login-user')
    template_name = 'accounts/change-password.html'
    form_class = PasswordChangeStyledForm

    def form_valid(self, form):
        messages.success(self.request, 'Your password was successfully updated.')
        return super().form_valid(form)


class ProfileDetails(LoginRequiredMixin, views.DetailView):
    model = UserModel
    template_name = 'accounts/profile-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_owner'] = self.request.user == self.object

        if self.object.user_type == 'teacher':
            # avg_rate logic (your existing code)
            trophies = Trophy.objects.filter(completed_by=self.object.pk).all()
            if trophies:
                avg_rate = mean([trophy.rate for trophy in list(trophies)])
                context['avg_rate'] = avg_rate
            else:
                context['avg_rate'] = None

            # NEW: specializations
            # Safer than assuming the profile always exists
            teacher_profile = getattr(self.object, "teacher_profile", None)
            context["specializations"] = (
                teacher_profile.specializations.all()
                if teacher_profile else []
            )

        return context



class ProfileEdit(LoginRequiredMixin, views.UpdateView):
    model = UserModel
    form_class = UserEditForm
    template_name = 'accounts/profile-edit.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('details-user', kwargs={'pk': self.object.pk})


class ProfileDelete(LoginRequiredMixin, views.DeleteView):
    model = UserModel
    template_name = 'accounts/profile-delete.html'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        if self.request.user != self.object:
            return redirect('details-user', pk=self.object.pk)

        return result


class TeacherSpecializationsView(LoginRequiredMixin, views.UpdateView):
    model = TeacherProfile
    form_class = TeacherSpecializationsForm
    template_name = "accounts/teacher-specializations.html"

    def dispatch(self, request, *args, **kwargs):
        # Only teachers can access this page
        if request.user.user_type != TypesOfUsers.teacher.value:
            return redirect("index")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        # Ensure profile exists (signals should create it, but this is safe)
        profile, _ = TeacherProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_success_url(self):
        return (
                self.request.POST.get("next")
                or self.request.GET.get("next")
                or reverse_lazy("index")
        )