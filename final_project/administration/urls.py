from django.urls import path, include

from final_project.administration.views import admin_index, AdminCreateUserView, AdminCreateGroupView, \
    AdminCreatePaperView, AdminCreateLessonView, AdminCreateCompletedPaperView, AdminCreateTrophyView, \
    AdminEditUserView, AdminListUserView, AdminDetailsUserView, AdminDeleteUserView, AdminListPaperView, \
    AdminEditPaperView, AdminDetailsPaperView, AdminDeletePaperView, AdminListLessonView, AdminDetailsLessonView, \
    AdminEditLessonView, AdminDeleteLessonView, AdminListCompletedView, AdminDetailsCompletedView, \
    AdminEditCompletedView, AdminDeleteCompletedView, AdminListTrophyView, AdminDetailsTrophyView, AdminEditTrophyView, \
    AdminDeleteTrophyView, AdminListMaterialsView, AdminCreateMaterialsView, AdminDetailsMaterialView, \
    AdminDeleteMaterialView, AdminEditMaterialView, AdminListGroupView, AdminDeleteGroupView, AdminEditGroupView

urlpatterns = (
    path('', admin_index, name='admin-index'),
    path('users/', include([
        path('add/', AdminCreateUserView.as_view(), name='admin-user-add'),
        path('list/', AdminListUserView.as_view(), name='admin-user-list'),
        path('edit/<int:pk>/', AdminEditUserView.as_view(), name='admin-user-edit'),
        path('details/<int:pk>/', AdminDetailsUserView.as_view(), name='admin-user-details'),
        path('delete/<int:pk>/', AdminDeleteUserView.as_view(), name='admin-user-delete')
    ])),
    path('group/', include([
        path('add/', AdminCreateGroupView.as_view(), name='admin-group-add'),
        path('list/', AdminListGroupView.as_view(), name='admin-group-list'),
        path('edit/<int:pk>/', AdminEditGroupView.as_view(), name='admin-group-edit'),
        path('delete/<int:pk>/', AdminDeleteGroupView.as_view(), name='admin-group-delete'),
    ])),
    path('term-paper/', include([
        path('add/', AdminCreatePaperView.as_view(), name='admin-paper-add'),
        path('list/', AdminListPaperView.as_view(), name='admin-paper-list'),
        path('edit/<int:pk>/', AdminEditPaperView.as_view(), name='admin-paper-edit'),
        path('details/<int:pk>/', AdminDetailsPaperView.as_view(), name='admin-paper-details'),
        path('delete/<int:pk>/', AdminDeletePaperView.as_view(), name='admin-paper-delete'),
    ])),
    path('lesson/', include([
        path('add/', AdminCreateLessonView.as_view(), name='admin-lesson-add'),
        path('list/', AdminListLessonView.as_view(), name='admin-lesson-list'),
        path('details/<int:pk>/', AdminDetailsLessonView.as_view(), name='admin-lesson-details'),
        path('edit/<int:pk>', AdminEditLessonView.as_view(), name='admin-lesson-edit'),
        path('delete/<int:pk>', AdminDeleteLessonView.as_view(), name='admin-lesson-delete'),
    ])),
    path('completed-papers/', include([
        path('add/', AdminCreateCompletedPaperView.as_view(), name='admin-completed-add'),
        path('list/', AdminListCompletedView.as_view(), name='admin-completed-list'),
        path('details/<int:pk>/', AdminDetailsCompletedView.as_view(), name='admin-completed-details'),
        path('edit/<int:pk>/', AdminEditCompletedView.as_view(), name='admin-completed-edit'),
        path('delete/<int:pk>/', AdminDeleteCompletedView.as_view(), name='admin-completed-delete'),
    ])),
    path('trophies/', include([
        path('add/', AdminCreateTrophyView.as_view(), name='admin-trophy-add'),
        path('list/', AdminListTrophyView.as_view(), name='admin-trophy-list'),
        path('details/<int:pk>/', AdminDetailsTrophyView.as_view(), name='admin-trophy-details'),
        path('edit<int:pk>/', AdminEditTrophyView.as_view(), name='admin-trophy-edit'),
        path('delete/<int:pk>/', AdminDeleteTrophyView.as_view(), name='admin-trophy-delete')

    ])),
    path('materials/', include([
        path('add/', AdminCreateMaterialsView.as_view(), name='admin-materials-add'),
        path('list/', AdminListMaterialsView.as_view(), name='admin-materials-list'),
        path('details/<int:pk>/', AdminDetailsMaterialView.as_view(), name='admin-material-details'),
        path('edit<int:pk>/', AdminEditMaterialView.as_view(), name='admin-material-edit'),
        path('delete/<int:pk>/', AdminDeleteMaterialView.as_view(), name='admin-material-delete')

    ])),
)
