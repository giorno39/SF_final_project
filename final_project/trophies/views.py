from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views
from django.utils.translation import gettext_lazy as _

from final_project.core.permissions_mixins import StudentRequiredMixin
from final_project.term_papers.models import TermPaper

from final_project.trophies.models import Trophy


class CreateTrophyView(StudentRequiredMixin, views.CreateView):
    model = Trophy
    template_name = 'trophies/trophy-add.html'
    fields = ('rate', 'comment')
    success_url = reverse_lazy('student-papers')

    def get_term_paper(self):
        return get_object_or_404(
            TermPaper,
            pk=self.kwargs['paper_pk'],
            user=self.request.user,
        )

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        term_paper = self.get_term_paper()

        form.instance.project = term_paper.title
        form.instance.completed_by = term_paper.taken_by
        form.fields['rate'].label = _('Rating')
        form.fields['comment'].label = _('Comment')

        form.fields['rate'].widget.attrs.setdefault(
            'placeholder',
            _('0 – 5')
        )

        form.fields['comment'].widget.attrs.update({
            'placeholder': _(
                'Describe the teacher’s communication, quality of work, and whether the paper was delivered on time. This helps us improve future recommendations.'
            ),
            'rows': 5,
        })
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk_paper'] = self.kwargs['paper_pk']
        return context

    def get(self, request, *args, **kwargs):
        term_paper = self.get_term_paper()

        if term_paper.rated:
            return render(self.request, 'trophies/trophy-already-rated.html')

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        term_paper = self.get_term_paper()

        if term_paper.rated:
            return render(self.request, 'trophies/trophy-already-rated.html')

        term_paper.rated = True
        term_paper.save()

        return super().form_valid(form)


class TeacherTrophies(views.ListView):
    model = Trophy
    template_name = 'trophies/trophy-list.html'
    context_object_name = 'trophies'

    def get_queryset(self):
        teacher_id = self.kwargs['teacher']
        return Trophy.objects.filter(completed_by_id=teacher_id)
