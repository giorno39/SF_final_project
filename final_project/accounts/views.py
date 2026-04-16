from statistics import mean

from django.contrib import messages
from django.contrib.auth import views as auth_views, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views import generic as views

from final_project.accounts.forms import (
    LoginForm,
    PasswordChangeStyledForm,
    UserCreateForm,
    UserEditForm,
    TeacherSpecializationsForm,
    TeacherSpecializationProofFormSet,
)
from final_project.accounts.models import (
    Specialization,
    TeacherProfile,
    TeacherSpecializationRequest,
    TypesOfUsers,
)
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
        response = super().form_valid(form)
        login(self.request, self.object)

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
            trophies = Trophy.objects.filter(completed_by=self.object.pk).all()
            if trophies:
                avg_rate = mean([trophy.rate for trophy in list(trophies)])
                context['avg_rate'] = avg_rate
            else:
                context['avg_rate'] = None

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


class TeacherSpecializationsView(LoginRequiredMixin, View):
    template_name = "accounts/teacher-specializations.html"
    session_key = "selected_specialization_ids"

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != TypesOfUsers.teacher.value:
            return redirect("index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        teacher_profile, _ = TeacherProfile.objects.get_or_create(user=request.user)

        initial_ids = list(
            teacher_profile.specialization_requests.exclude(specialization__in=teacher_profile.specializations.all())
            .values_list("specialization_id", flat=True)
        )

        form = TeacherSpecializationsForm(
            initial={"specializations": initial_ids}
        )
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = TeacherSpecializationsForm(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        specialization_ids = [
            specialization.id
            for specialization in form.cleaned_data["specializations"]
        ]
        request.session[self.session_key] = specialization_ids

        return redirect("teacher-specialization-proofs")


class TeacherSpecializationProofUploadView(LoginRequiredMixin, View):
    template_name = "accounts/teacher-specialization-proofs.html"
    session_key = "selected_specialization_ids"

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != TypesOfUsers.teacher.value:
            return redirect("index")
        return super().dispatch(request, *args, **kwargs)

    def get_selected_specializations(self, request):
        specialization_ids = request.session.get(self.session_key, [])
        return list(Specialization.objects.filter(id__in=specialization_ids).order_by("name"))

    def get(self, request, *args, **kwargs):
        specializations = self.get_selected_specializations(request)
        if not specializations:
            messages.warning(request, "Please select your specializations first.")
            return redirect("teacher-specializations")

        formset = TeacherSpecializationProofFormSet(
            initial=[{} for _ in specializations]
        )
        paired_forms = list(zip(specializations, formset.forms))

        return render(
            request,
            self.template_name,
            {
                "formset": formset,
                "paired_forms": paired_forms,
                "specializations": specializations,
            },
        )

    def post(self, request, *args, **kwargs):
        specializations = self.get_selected_specializations(request)
        if not specializations:
            messages.warning(request, "Please select your specializations first.")
            return redirect("teacher-specializations")

        formset = TeacherSpecializationProofFormSet(
            request.POST,
            request.FILES,
            initial=[{} for _ in specializations],
        )

        if len(formset.forms) != len(specializations):
            messages.error(request, "Something went wrong. Please try again.")
            return redirect("teacher-specializations")

        all_valid = True
        for form in formset.forms:
            form.full_clean()
            if not form.cleaned_data.get("proof_file"):
                form.add_error("proof_file", "Please attach a proof file.")
                all_valid = False
            elif form.errors:
                all_valid = False

        if not formset.is_valid() or not all_valid:
            paired_forms = list(zip(specializations, formset.forms))
            return render(
                request,
                self.template_name,
                {
                    "formset": formset,
                    "paired_forms": paired_forms,
                    "specializations": specializations,
                },
            )

        teacher_profile, _ = TeacherProfile.objects.get_or_create(user=request.user)

        for specialization, form in zip(specializations, formset.forms):
            proof_file = form.cleaned_data["proof_file"]

            TeacherSpecializationRequest.objects.update_or_create(
                teacher=teacher_profile,
                specialization=specialization,
                defaults={
                    "proof_file": proof_file,
                    "status": "pending",
                    "reviewer_note": "",
                    "reviewed_by": None,
                    "reviewed_at": None,
                },
            )

        request.session.pop(self.session_key, None)
        messages.success(
            request,
            "Your specialization requests were submitted for review.",
        )
        return redirect("index")