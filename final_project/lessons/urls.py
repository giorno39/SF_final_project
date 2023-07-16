from django.urls import path

from final_project.lessons.views import CreateLessonView, LessonIndexView, LessonDetailsView, LessonEditView, \
    OwnLessonView, LessonDeleteView

urlpatterns = (
    path('', LessonIndexView.as_view(), name='lesson-index'),
    path('add/', CreateLessonView.as_view(), name='lesson-add'),
    path('details/<int:pk>', LessonDetailsView.as_view(), name='lesson-details'),
    path('edit/<int:pk>', LessonEditView.as_view(), name='lesson-edit'),
    path('my-lessons/', OwnLessonView.as_view(), name='own-lesson-index'),
    path('delete/<int:pk>', LessonDeleteView.as_view(), name='lesson-delete')
)