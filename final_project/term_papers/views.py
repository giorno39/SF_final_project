from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
import os

from final_project import settings
from final_project.term_papers.forms import TermPaperCreateForm
from final_project.term_papers.models import TermPaper

UserModel = get_user_model()


class TermPaperIndexView(views.ListView):
    model = TermPaper
    template_name = 'term-papers/term-paper-index.html'

    def get_queryset(self, *args, **kwargs):
        queryset = TermPaper.objects \
            .filter(taken_by=None) \
            .all()

        return queryset


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
        # TODO check how to acces related objects
        c_user = UserModel.objects. \
            filter(pk=self.request.user.pk). \
            get()

        if c_user.user_type == 'teacher':
            return redirect('index')

        return result


class TermPaperEditView(views.UpdateView):
    model = TermPaper
    fields = ('title', 'death_line', 'price_cap',)
    template_name = 'term-papers/term-paper-edit.html'
#TODO if accessed by someone that is not the creator it must be redirected
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
    #TODO delete the file as well as the paper
    model = TermPaper
    template_name = 'term-papers/term-paper-delete.html'
    success_url = reverse_lazy('term-paper-index')


def open_file(request, pk):
    term_paper = TermPaper.objects.filter(pk=pk).get()
    file_name = str(term_paper.content)
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response


@login_required
def take_term_paper(request, pk):
    c_user = UserModel.objects. \
        filter(pk=request.user.pk). \
        get()

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

    def get_success_url(self):
        return reverse_lazy('teacher-papers')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.completed = True

        return form

    #TODO redirect if accessed by someone the is not the appropriate teacher

