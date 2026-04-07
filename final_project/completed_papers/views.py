from django.http import FileResponse
from django.views import generic as views
import os

from final_project import settings
from final_project.completed_papers.forms import CompletedPaperSearchForm
from final_project.completed_papers.models import CompletedPaper

def _completed_paper_feed_querystring(request):
    q = request.GET.copy()
    q.pop('page', None)
    return q.urlencode()

class CompletedPapersIndexView(views.ListView):
    model = CompletedPaper
    template_name = 'completed_paper/completed-paper-index.html'
    paginate_by = 4

    def get_queryset(self):
        search_form = CompletedPaperSearchForm(self.request.GET)
        search_pattern = None
        specialization = None

        completed_papers = (
            CompletedPaper.objects
            .select_related('completed_by')
            .prefetch_related('specializations')
        )

        if search_form.is_valid():
            search_pattern = search_form.cleaned_data.get('completed_title')
            specialization = search_form.cleaned_data.get('specialization')

        if search_pattern:
            completed_papers = completed_papers.filter(title__icontains=search_pattern)

        if specialization:
            completed_papers = completed_papers.filter(specializations=specialization)

        return completed_papers.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = CompletedPaperSearchForm(self.request.GET)
        context['completed_paper_feed_title'] = 'Completed Papers Feed'
        context['get_params'] = _completed_paper_feed_querystring(self.request)
        return context


class CompletedPapersDetailsView(views.DetailView):
    model = CompletedPaper
    template_name = 'completed_paper/completed-paper-details.html'


def open_completed_paper(request, pk):
    term_paper = CompletedPaper.objects.filter(pk=pk).get()
    file_name = str(term_paper.content)
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response