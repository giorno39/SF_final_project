from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from final_project.term_papers.models import TermPaper

from final_project.trophies.models import Trophy


# Create your views here.

class CreateTrophyView(views.CreateView):
    model = Trophy
    template_name = 'trophies/trophy-add.html'
    fields = ('rate',)
    success_url = reverse_lazy('student-papers')


    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        term_paper = TermPaper.objects \
            .filter(pk=self.kwargs['paper_pk']) \
            .get()


        form.instance.project = term_paper.title
        form.instance.completed_by = term_paper.taken_by


        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk_paper'] = self.kwargs['paper_pk']

        return context

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)

        term_paper = TermPaper.objects \
            .filter(pk=self.kwargs['paper_pk']) \
            .get()

        if term_paper.rated:
            return render(self.request, 'trophies/trophy-already-rated.html')

        return result


    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)

        term_paper = TermPaper.objects \
            .filter(pk=self.kwargs['paper_pk']) \
            .get()

        term_paper.rated = True
        term_paper.save()

        return result

