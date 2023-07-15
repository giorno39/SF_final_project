from django.urls import path

from final_project.trophies.views import CreateTrophyView

urlpatterns = (
    path('rate/<int:paper_pk>', CreateTrophyView.as_view(), name='trophy-add'),
)