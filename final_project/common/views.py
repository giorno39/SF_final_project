from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic as views

from final_project.core.funcs import get_user_by_id
from final_project.term_papers.forms import TermPaperSearchForm
from final_project.term_papers.models import TermPaper

# Create your views here.

UserModel = get_user_model()


def index(request):
    if request.user.is_authenticated:
        return render(request, 'common/index-accounts.html')
    else:
        return render(request, 'base/base.html')


class StudentPaperView(LoginRequiredMixin, views.ListView):
    model = TermPaper
    template_name = 'term-papers/term-paper-index.html'


    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        c_user = get_user_by_id(self.request.user.pk)

        if c_user.user_type == 'teacher':
            return redirect('teacher-papers')

        return result

    def get_queryset(self):
        queryset = TermPaper.objects.filter(user_id=self.request.user.pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_form'] = TermPaperSearchForm(self.request.GET)

        return context


class TeacherPaperView(LoginRequiredMixin, views.ListView):
    model = TermPaper
    template_name = 'teacher/teacher-taken-papers.html'

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        c_user = get_user_by_id(self.request.user.pk)

        if c_user.user_type == 'student':
            return redirect('student-papers')

        return result

    def get_queryset(self):
        queryset = TermPaper.objects.filter(taken_by=self.request.user.pk, completed=False)
        return queryset
