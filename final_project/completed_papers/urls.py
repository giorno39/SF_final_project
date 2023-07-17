from django.urls import path

from final_project.completed_papers.views import CompletedPapersIndexView, open_completed_paper, \
    CompletedPapersDetailsView

urlpatterns = (
    path('', CompletedPapersIndexView.as_view(), name='completed_paper-index'),
    path('open-completed_paper/<int:pk>', open_completed_paper, name='completed_paper-open'),
    path('details/<int:pk>', CompletedPapersDetailsView.as_view(), name='completed-paper-details')
)
