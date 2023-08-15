from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
import os

from final_project import settings
from final_project.completed_papers.models import CompletedPaper
from final_project.core.funcs import get_user_by_id
from final_project.term_papers.forms import TermPaperCreateForm, TermPaperSearchForm
from final_project.term_papers.models import TermPaper

UserModel = get_user_model()


class TermPaperIndexView(views.ListView):
    model = TermPaper
    template_name = 'term-papers/term-paper-index.html'
    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        search_form = TermPaperSearchForm(self.request.GET)
        search_pattern = None
        if search_form.is_valid():
            search_pattern = search_form.cleaned_data['paper_title']

        queryset = TermPaper.objects \
            .filter(taken_by=None, completed=False, death_line__gt=datetime.today()) \
            .all()

        if search_pattern:
            queryset = queryset.filter(title__icontains=search_pattern)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_form'] = TermPaperSearchForm(self.request.GET)

        return context


class TermPaperDetailsView(views.DetailView):
    model = TermPaper
    template_name = 'term-papers/term-paper-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.request.user.pk == self.object.user_id
        context['is_taken'] = self.object.taken_by

        return context


class TermPaperCreateView(views.CreateView):
    model = TermPaper
    form_class = TermPaperCreateForm
    template_name = 'term-papers/term-paper-add.html'

    def get_success_url(self):
        return reverse_lazy('term-paper-details', kwargs={
            'pk': self.object.pk
        })

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.user = self.request.user

        return form

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        c_user = get_user_by_id(self.request.user.pk)

        if c_user.user_type == 'teacher':
            return redirect('index')

        return result


class TermPaperEditView(views.UpdateView):
    model = TermPaper
    fields = ('title', 'death_line', 'price_cap',)
    template_name = 'term-papers/term-paper-edit.html'

    def get_success_url(self):
        return reverse_lazy('term-paper-details', kwargs={
            'pk': self.object.pk,
        })

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        if self.request.user != self.object.user:
            result = reverse_lazy('term-paper-details', kwargs={
                'pk': self.object.pk,
            })

            return redirect(result)

        return result


class TermPaperDeleteView(views.DeleteView):
    model = TermPaper
    template_name = 'term-papers/term-paper-delete.html'
    success_url = reverse_lazy('term-paper-index')

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)

        if self.request.user != self.object.user:
            result = reverse_lazy('term-paper-details', kwargs={
                'pk': self.object.pk,
            })

            return redirect(result)

        return result

    def post(self, *args, **kwargs):
        result = super().post(*args, **kwargs)

        path = os.path.join(settings.MEDIA_ROOT, str(self.object.content))
        os.remove(path)

        return result


def open_file(request, pk):
    term_paper = TermPaper.objects.filter(pk=pk).get()
    file_name = str(term_paper.content)
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response


@login_required
def take_term_paper(request, pk):
    c_user = get_user_by_id(request.user.pk)

    if c_user.user_type == 'student':
        return redirect('term-paper-details', pk=pk)

    term_paper = TermPaper.objects \
        .filter(pk=pk) \
        .get()

    term_paper.taken_by_id = request.user.pk
    term_paper.save()
    return redirect('term-paper-details', pk=pk)


class CompletePaper(views.UpdateView):
    model = TermPaper
    template_name = 'teacher/teacher-complete-paper.html'
    fields = ('content',)
    is_updatable = None

    def get_success_url(self):
        return reverse_lazy('teacher-papers')

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)

        if self.is_updatable:
            self.object.completed = True

            CompletedPaper.objects.create(
                title=self.object.title,
                subject=self.object.subject,
                university=self.object.university,
                content=self.object.content,
                completed_by=self.object.taken_by,
            )

            self.object.save()

        return result

    def get(self, *args, **kwargs):
        result = super().get(*args, **kwargs)

        if self.request.user != self.object.taken_by:
            result = reverse_lazy('term-paper-details', kwargs={
                'pk': self.object.pk,
            })

            return redirect(result)

        return result

    def form_valid(self, form, *args, **kwargs):

        initial_data = self.get_object().__dict__.copy()

        cleaned_data = form.cleaned_data

        if initial_data['content'] == cleaned_data['content']:
            self.is_updatable = False
            return render(self.request, 'common/no-changes_detected.html')

        self.is_updatable = True

        return super().form_valid(form)
