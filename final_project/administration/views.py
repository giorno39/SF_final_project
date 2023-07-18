from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views import generic as views

from final_project.completed_papers.models import CompletedPaper
from final_project.core.decorators import allow_groups
from final_project.lessons.models import Lesson
from final_project.term_papers.models import TermPaper
from final_project.trophies.models import Trophy

UserModel = get_user_model()


@login_required
def admin_index(request):
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'administration/administration-index.html')
    else:
        return HttpResponse("You don't have permissions to visit this page")


# ADMIN LIST VIEWS
class AdminListUserView(views.ListView):
    model = UserModel
    template_name = 'administration/users/user-list.html'


class AdminListPaperView(views.ListView):
    model = TermPaper
    template_name = 'administration/term-papers/term-paper-list.html'


class AdminListLessonView(views.ListView):
    model = Lesson
    template_name = 'administration/lessons/lesson-list.html'


class AdminListCompletedView(views.ListView):
    model = CompletedPaper
    template_name = 'administration/completed-papers/completed-list.html'


# CREATE ADMIN VIEWS
class AdminCreateUserView(views.CreateView):
    model = UserModel
    template_name = 'administration/users/add-user.html'
    fields = '__all__'
    success_url = reverse_lazy('admin-index')


class AdminCreateGroupView(views.CreateView):
    model = Group
    success_url = reverse_lazy('admin-index')
    template_name = 'administration/groups/add-group.html'
    fields = '__all__'


class AdminCreatePaperView(views.CreateView):
    model = TermPaper
    success_url = reverse_lazy('admin-index')
    template_name = 'administration/term-papers/add-term-paper.html'
    fields = '__all__'


class AdminCreateLessonView(views.CreateView):
    model = Lesson
    success_url = reverse_lazy('admin-index')
    template_name = 'administration/lessons/add-lesson.html'
    fields = '__all__'


class AdminCreateCompletedPaperView(views.CreateView):
    model = CompletedPaper
    success_url = reverse_lazy('admin-index')
    template_name = 'administration/completed-papers/add-completed-paper.html'
    fields = '__all__'


# TODO when we need to add a tropy, make a custom form, with choices equal to teachers only for the field completed_by
class AdminCreateTrophyView(views.CreateView):
    model = Trophy
    success_url = reverse_lazy('admin-index')
    template_name = 'administration/trophies/add-trophy.html'
    fields = '__all__'


# CHAGE ADMIN VIEWS
# TODO change the succes url to the details, when avaiable
class AdminEditUserView(views.UpdateView):
    model = UserModel
    template_name = 'administration/users/change-user.html'
    # TODO exclude password from change options
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('admin-user-details', kwargs={
            'pk': self.object.pk
        })


class AdminEditPaperView(views.UpdateView):
    model = TermPaper
    fields = '__all__'
    template_name = 'administration/term-papers/change-paper.html'

    def get_success_url(self):
        return reverse_lazy('admin-paper-details', kwargs={
            'pk': self.object.pk
        })


class AdminEditLessonView(views.UpdateView):
    model = Lesson
    fields = '__all__'
    template_name = 'administration/lessons/change-lesson.html'

    def get_success_url(self):
        return reverse_lazy('admin-lesson-details', kwargs={
            'pk': self.object.pk
        })


class AdminEditCompletedView(views.UpdateView):
    model = CompletedPaper
    fields = '__all__'
    template_name = 'administration/completed-papers/change-completed-paper.html'

    def get_success_url(self):
        return reverse_lazy('admin-completed-details', kwargs={
            'pk': self.object.pk
        })


# ADMIN DETAILS VIEWS

class AdminDetailsUserView(views.DetailView, UserPassesTestMixin):
    model = UserModel
    template_name = 'administration/users/details-user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['groups'] = self.object.groups.all()

        return context


class AdminDetailsPaperView(views.DetailView):
    model = TermPaper
    template_name = 'administration/term-papers/details-paper.html'


class AdminDetailsLessonView(views.DetailView):
    model = Lesson
    template_name = 'administration/lessons/details-lesson.html'


class AdminDetailsCompletedView(views.DetailView):
    model = CompletedPaper
    template_name = 'administration/completed-papers/details-completed-paper.html'


# ADMIN DELETE VIEWS
class AdminDeleteUserView(views.DeleteView):
    model = UserModel
    template_name = 'administration/users/delete-user.html'
    success_url = reverse_lazy('admin-user-list')


class AdminDeletePaperView(views.DeleteView):
    model = TermPaper
    template_name = 'administration/term-papers/delete-paper.html'
    success_url = reverse_lazy('admin-paper-list')


class AdminDeleteLessonView(views.DeleteView):
    model = Lesson
    template_name = 'administration/lessons/delete-lesson.html'
    success_url = reverse_lazy('admin-lesson-list')


class AdminDeleteCompletedView(views.DeleteView):
    model = CompletedPaper
    template_name = 'administration/completed-papers/delete-completed-paper.html'
    success_url = reverse_lazy('admin-completed-list')
