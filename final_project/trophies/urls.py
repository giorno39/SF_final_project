from django.urls import path

from final_project.trophies.views import CreateTrophyView, TeacherTrophies

urlpatterns = (
    path('rate/<int:paper_pk>', CreateTrophyView.as_view(), name='trophy-add'),
    path('trophies/<int:teacher>', TeacherTrophies.as_view(), name='teacher-trophy'),
)