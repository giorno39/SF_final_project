from django.http import FileResponse
from django.shortcuts import render
from django.views import generic as views
import os

from final_project import settings
from final_project.completed_papers.models import CompletedPaper


# Create your views here.

class CompletedPapersIndexView(views.ListView):
    model = CompletedPaper
    template_name = 'completed_paper/completed-paper-index.html'


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

