from statistics import mean

from django.contrib.auth import views as auth_views, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.checks import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from final_project.accounts.forms import UserCreateForm, UserEditForm
from django.contrib import messages
from final_project.trophies.models import Trophy

UserModel = get_user_model()


class SignInView(auth_views.LoginView):
    template_name = 'accounts/profile-login.html'


class SignUpView(views.CreateView):
    model = UserModel
    form_class = UserCreateForm
    template_name = 'accounts/profile-register.html'
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        login(request, self.object)
        return response


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('index')


class ChangePasswordView(auth_views.PasswordChangeView):
    success_url = reverse_lazy('login-user')
    template_name = 'accounts/change-password.html'

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
            trophies = Trophy.objects.filter(completed_by=self.object.pk).all()
            if trophies:
                avg_rate = mean([trophy.rate for trophy in list(trophies)])

                context['avg_rate'] = avg_rate
            else:
                context['avg_rate'] = None

        return context


class ProfileEdit(LoginRequiredMixin, views.UpdateView):
    model = UserModel
    class_form = UserEditForm
    fields = ('first_name', 'last_name', 'email')
    template_name = 'accounts/profile-edit.html'

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        if self.request.user != self.object:
            return redirect('details-user', pk=self.object.pk)

        return result

    def get_success_url(self):
        return reverse_lazy('details-user', kwargs={
            'pk': self.object.pk
        })


class ProfileDelete(LoginRequiredMixin, views.DeleteView):
    model = UserModel
    template_name = 'accounts/profile-delete.html'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        if self.request.user != self.object:
            return redirect('details-user', pk=self.object.pk)

        return result
