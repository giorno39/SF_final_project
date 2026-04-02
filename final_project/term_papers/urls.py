from django.urls import path

from final_project.term_papers.views import TermPaperIndexView, TermPaperDetailsView, TermPaperCreateView, \
    TermPaperEditView, TermPaperDeleteView, open_file, take_term_paper, CompletePaper, \
    TermPaperRequestTeacherListView, send_term_paper_request, TeacherTermPaperRequestsListView, \
    accept_term_paper_request, decline_term_paper_request, unassign_term_paper, generate_term_paper_description

urlpatterns = (
    path('', TermPaperIndexView.as_view(), name='term-paper-index'),
    path('add-term-paper/', TermPaperCreateView.as_view(), name='term-paper-add'),
    path('details/<int:pk>/', TermPaperDetailsView.as_view(), name='term-paper-details'),
    path('edit/<int:pk>', TermPaperEditView.as_view(), name='term-paper-edit'),
    path('delete/<int:pk>', TermPaperDeleteView.as_view(), name='term-paper-delete'),
    path('download-file/<int:pk>/', open_file, name='term-paper-file-open'),
    path('take/<int:pk>/', take_term_paper, name='term-paper-take'),
    path('complete-paper/<int:pk>', CompletePaper.as_view(), name='term-paper-complete'),
    path('term-paper/<int:pk>/untake/', unassign_term_paper, name='term-paper-untake'),

    path('<int:pk>/request-teacher/', TermPaperRequestTeacherListView.as_view(), name='term-paper-request-teacher'),
    path('<int:pk>/request-teacher/<int:teacher_pk>/', send_term_paper_request, name='send-term-paper-request'),

    path('teacher/requests/', TeacherTermPaperRequestsListView.as_view(), name='teacher-term-paper-requests'),
    path('teacher/requests/<int:request_pk>/accept/', accept_term_paper_request, name='accept-term-paper-request'),
    path('teacher/requests/<int:request_pk>/decline/', decline_term_paper_request, name='decline-term-paper-request'),
    path('generate-description/',generate_term_paper_description,name='generate-term-paper-description',),
)