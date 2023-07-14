from django.contrib.auth import get_user_model
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


class TermPaperDetailsView(views.DetailView):
    model = TermPaper
    template_name = 'term-papers/term-paper-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.request.user.pk == self.object.user_id

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

    def get_success_url(self):
        return reverse_lazy('term-paper-details', kwargs={
            'pk': self.object.pk,
        })


class TermPaperDeleteView(views.DeleteView):
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
