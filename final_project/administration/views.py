from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group
from django.core import exceptions
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views import generic as views

from final_project.administration.forms import AdminUserCreateForm, AdminLessonCreateForm, AdminTermPaperCreateForm, \
    AdminCompletedPaperCreateForm, AdminTrophyCreateForm
from final_project.completed_papers.models import CompletedPaper
from final_project.core.decorators import allow_groups
from final_project.lessons.models import Lesson
from final_project.term_papers.models import TermPaper
from final_project.trophies.models import Trophy
from final_project.useful_materials.models import Materials

UserModel = get_user_model()


@login_required
def admin_index(request):
    context = {
        'add_users': request.user.has_perm('accounts.add_appuser'),
        'add_papers': request.user.has_perm('term_papers.add_termpaper'),
        'add_lessons': request.user.has_perm('lessons.add_Lesson'),
        'add_completed': request.user.has_perm('completed_paper.add_completedpaper'),
        'add_trophies': request.user.has_perm('trophies.add_trophy'),
        'add_materials': request.user.has_perm('useful_materials.add_materials'),
        'add_groups': request.user.has_perm('auth.add_group')
    }

    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'administration/administration-index.html', context=context)
    else:
        return HttpResponse("You don't have permissions to visit this page")


# ADMIN LIST VIEWS
@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminListUserView(views.ListView):
    model = UserModel
    template_name = 'administration/users/user-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['change_user'] = self.request.user.has_perm('accounts.change_appuser')
        context['view_user'] = self.request.user.has_perm('accounts.view_appuser')

        return context


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminListPaperView(views.ListView):
    model = TermPaper
    template_name = 'administration/term-papers/term-paper-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['change_paper'] = self.request.user.has_perm('term_papers.change_termpaper')
        context['view_paper'] = self.request.user.has_perm('term_papers.view_termpaper')

        return context


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminListLessonView(views.ListView):
    model = Lesson
    template_name = 'administration/lessons/lesson-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['change_lesson'] = self.request.user.has_perm('lessons.change_lesson')
        context['view_lesson'] = self.request.user.has_perm('lessons.view_lesson')

        return context


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminListCompletedView(views.ListView):
    model = CompletedPaper
    template_name = 'administration/completed-papers/completed-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['change_completed'] = self.request.user.has_perm('completed_papers.change_completedpaper')
        context['view_completed'] = self.request.user.has_perm('completed_papers.view_completedpaper')

        return context


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminListTrophyView(views.ListView):
    model = Trophy
    template_name = 'administration/trophies/trophy-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['change_trophy'] = self.request.user.has_perm('trophies.change_trophy')
        context['view_trophy'] = self.request.user.has_perm('trophies.view_trophy')

        return context


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminListMaterialsView(views.ListView):
    model = Materials
    template_name = 'administration/materials/materials-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['change_materials'] = self.request.user.has_perm('useful_materials.change_materials')
        context['view_materials'] = self.request.user.has_perm('useful_materials.view_materials')

        return context


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminListGroupView(views.ListView):
    model = Group
    template_name = 'administration/groups/group-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['change_group'] = self.request.user.has_perm('auth.change_group')
        context['view_group'] = self.request.user.has_perm('auth.view_group')

        return context


# CREATE ADMIN VIEWS
@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminCreateUserView(views.CreateView):
    model = UserModel
    template_name = 'administration/users/add-user.html'
    form_class = AdminUserCreateForm
    success_url = reverse_lazy('admin-index')


@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminCreateGroupView(views.CreateView):
    model = Group
    success_url = reverse_lazy('admin-index')
    template_name = 'administration/groups/add-group.html'
    fields = '__all__'


@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminCreatePaperView(views.CreateView):
    model = TermPaper
    success_url = reverse_lazy('admin-index')
    template_name = 'administration/term-papers/add-term-paper.html'
    # fields = '__all__'
    form_class = AdminTermPaperCreateForm

@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminCreateLessonView(views.CreateView):
    model = Lesson
    success_url = reverse_lazy('admin-index')
    template_name = 'administration/lessons/add-lesson.html'
    form_class = AdminLessonCreateForm


@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminCreateCompletedPaperView(views.CreateView):
    model = CompletedPaper
    success_url = reverse_lazy('admin-index')
    template_name = 'administration/completed-papers/add-completed-paper.html'
    # fields = '__all__'
    form_class = AdminCompletedPaperCreateForm

@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminCreateTrophyView(views.CreateView):
    model = Trophy
    success_url = reverse_lazy('admin-index')
    template_name = 'administration/trophies/add-trophy.html'
    # fields = '__all__'
    form_class = AdminTrophyCreateForm

@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminCreateMaterialsView(views.CreateView):
    model = Materials
    success_url = reverse_lazy('admin-index')
    template_name = 'administration/materials/add-material.html'
    fields = '__all__'


# CHAGE ADMIN VIEWS
@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminEditUserView(views.UpdateView):
    model = UserModel
    template_name = 'administration/users/change-user.html'
    fields = ('last_login', 'is_superuser', 'groups', 'user_permissions', 'username', 'is_staff', 'is_active',
              'date_joined', 'first_name', 'last_name', 'email')

    def get_success_url(self):
        return reverse_lazy('admin-user-details', kwargs={
            'pk': self.object.pk
        })


@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminEditPaperView(views.UpdateView):
    model = TermPaper
    fields = '__all__'
    template_name = 'administration/term-papers/change-paper.html'

    def get_success_url(self):
        return reverse_lazy('admin-paper-details', kwargs={
            'pk': self.object.pk
        })


@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminEditLessonView(views.UpdateView):
    model = Lesson
    fields = '__all__'
    template_name = 'administration/lessons/change-lesson.html'

    @method_decorator(allow_groups(groups=['None']), name='dispatch')
    def get_success_url(self):
        return reverse_lazy('admin-lesson-details', kwargs={
            'pk': self.object.pk
        })


@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminEditCompletedView(views.UpdateView):
    model = CompletedPaper
    fields = '__all__'
    template_name = 'administration/completed-papers/change-completed-paper.html'

    def get_success_url(self):
        return reverse_lazy('admin-completed-details', kwargs={
            'pk': self.object.pk
        })


@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminEditTrophyView(views.UpdateView):
    model = Trophy
    fields = '__all__'
    template_name = 'administration/trophies/change-trophy.html'

    def get_success_url(self):
        return reverse_lazy('admin-trophy-details', kwargs={
            'pk': self.object.pk
        })


@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminEditMaterialView(views.UpdateView):
    model = Materials
    fields = '__all__'
    template_name = 'administration/materials/change-material.html'

    def get_success_url(self):
        return reverse_lazy('admin-material-details', kwargs={
            'pk': self.object.pk
        })


@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminEditGroupView(views.UpdateView):
    model = Group
    fields = '__all__'
    template_name = 'administration/groups/change-group.html'


# ADMIN DETAILS VIEWS
@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminDetailsUserView(views.DetailView, UserPassesTestMixin):
    model = UserModel
    template_name = 'administration/users/details-user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['groups'] = self.object.groups.all()

        return context


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminDetailsPaperView(views.DetailView):
    model = TermPaper
    template_name = 'administration/term-papers/details-paper.html'


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminDetailsLessonView(views.DetailView):
    model = Lesson
    template_name = 'administration/lessons/details-lesson.html'


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminDetailsCompletedView(views.DetailView):
    model = CompletedPaper
    template_name = 'administration/completed-papers/details-completed-paper.html'


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminDetailsTrophyView(views.DetailView):
    model = Trophy
    template_name = 'administration/trophies/details-trophy.html'


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminDetailsMaterialView(views.DetailView):
    model = Materials
    template_name = 'administration/materials/details-material.html'


# ADMIN DELETE VIEWS
@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminDeleteUserView(views.DeleteView):
    model = UserModel
    template_name = 'administration/users/delete-user.html'
    success_url = reverse_lazy('admin-user-list')


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminDeletePaperView(views.DeleteView):
    model = TermPaper
    template_name = 'administration/term-papers/delete-paper.html'
    success_url = reverse_lazy('admin-paper-list')


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminDeleteLessonView(views.DeleteView):
    model = Lesson
    template_name = 'administration/lessons/delete-lesson.html'
    success_url = reverse_lazy('admin-lesson-list')


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminDeleteCompletedView(views.DeleteView):
    model = CompletedPaper
    template_name = 'administration/completed-papers/delete-completed-paper.html'
    success_url = reverse_lazy('admin-completed-list')


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminDeleteTrophyView(views.DeleteView):
    model = Trophy
    template_name = 'administration/trophies/delete-trophy.html'
    success_url = reverse_lazy('admin-trophy-list')


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminDeleteMaterialView(views.DeleteView):
    model = Materials
    template_name = 'administration/materials/delete-material.html'
    success_url = reverse_lazy('admin-materials-list')


@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminDeleteGroupView(views.DeleteView):
    model = Group
    template_name = 'administration/groups/delete-group.html'
    success_url = reverse_lazy('admin-group-list')
