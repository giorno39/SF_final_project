from django.urls import path

from final_project.common.views import index, StudentPaperView, TeacherPaperView

urlpatterns = (
    path('', index, name='index'),
    path('student-papers/', StudentPaperView.as_view(), name='student-papers'),
    path('teacher-papers/', TeacherPaperView.as_view(), name='teacher-papers'),
)
