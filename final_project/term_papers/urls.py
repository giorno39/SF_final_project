from django.urls import path

from final_project.term_papers.views import TermPaperIndexView, TermPaperDetailsView, TermPaperCreateView, \
    TermPaperEditView, TermPaperDeleteView, open_file, take_term_paper, CompletePaper

urlpatterns = (
    path('', TermPaperIndexView.as_view(), name='term-paper-index'),
    path('add-term-paper/', TermPaperCreateView.as_view(), name='term-paper-add'),
    path('details/<int:pk>/', TermPaperDetailsView.as_view(), name='term-paper-details'),
    path('edit/<int:pk>', TermPaperEditView.as_view(), name='term-paper-edit'),
    path('delete/<int:pk>', TermPaperDeleteView.as_view(), name='term-paper-delete'),
    path('download-file/<int:pk>/', open_file, name='term-paper-file-open'),
    path('take/<int:pk>/', take_term_paper, name='term-paper-take'),
    path('complete-paper/<int:pk>', CompletePaper.as_view(), name='term-paper-complete'),
)
