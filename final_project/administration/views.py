from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views import generic as views

from final_project.administration.forms import AdminUserCreateForm
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
        'add_users': request.user.has_perm('accounts.add_AppUser'),
        'add_papers': request.user.has_perm('accounts.add_TermPaper'),
        'add_lessons': request.user.has_perm('accounts.add_Lesson'),
        'add_completed': request.user.has_perm('accounts.add_CompletedPaper'),
        'add_trophies': request.user.has_perm('accounts.add_Trophy'),
        'add_materials': request.user.has_perm('accounts.add_Materials'),
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


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminListPaperView(views.ListView):
    model = TermPaper
    template_name = 'administration/term-papers/term-paper-list.html'


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminListLessonView(views.ListView):
    model = Lesson
    template_name = 'administration/lessons/lesson-list.html'


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminListCompletedView(views.ListView):
    model = CompletedPaper
    template_name = 'administration/completed-papers/completed-list.html'


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminListTrophyView(views.ListView):
    model = Trophy
    template_name = 'administration/trophies/trophy-list.html'


@method_decorator(allow_groups(groups=['sanity_checker']), name='dispatch')
class AdminListMaterialsView(views.ListView):
    model = Materials
    template_name = 'administration/materials/materials-list.html'


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
    fields = '__all__'


@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminCreateLessonView(views.CreateView):
    model = Lesson
    success_url = reverse_lazy('admin-index')
    template_name = 'administration/lessons/add-lesson.html'
    fields = '__all__'


@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminCreateCompletedPaperView(views.CreateView):
    model = CompletedPaper
    success_url = reverse_lazy('admin-index')
    template_name = 'administration/completed-papers/add-completed-paper.html'
    fields = '__all__'


@method_decorator(allow_groups(groups=['None']), name='dispatch')
# TODO when we need to add a tropy, make a custom form, with choices equal to teachers only for the field completed_by
class AdminCreateTrophyView(views.CreateView):
    model = Trophy
    success_url = reverse_lazy('admin-index')
    template_name = 'administration/trophies/add-trophy.html'
    fields = '__all__'


@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminCreateMaterialsView(views.CreateView):
    model = Materials
    success_url = reverse_lazy('admin-index')
    template_name = 'administration/materials/add-materials.html'
    fields = '__all__'


# CHAGE ADMIN VIEWS
@method_decorator(allow_groups(groups=['None']), name='dispatch')
class AdminEditUserView(views.UpdateView):
    model = UserModel
    template_name = 'administration/users/change-user.html'
    # TODO exclude password from change options
    fields = '__all__'

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


# ADMIN DETAILS VIEWS
@method_decorator(allow_groups(groups=['None']), name='dispatch')
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
