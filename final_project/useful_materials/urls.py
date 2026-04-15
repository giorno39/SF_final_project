from django.urls import path

from final_project.useful_materials.views import MaterialsIndexView, MaterialCreateView, MaterialDetailsView, \
    download_completed_paper, MaterialEditView, MaterialDeleteView, add_material_comment, toggle_material_comment_like

urlpatterns = (
    path('', MaterialsIndexView.as_view(), name='materials-index'),
    path('add/', MaterialCreateView.as_view(), name='materials-add'),
    path('details/<int:pk>', MaterialDetailsView.as_view(), name='materials-details'),
    path('download-file/<int:pk>', download_completed_paper, name='materials-download'),
    path('edit/<int:pk>', MaterialEditView.as_view(), name='materials-edit'),
    path('delete/<int:pk>', MaterialDeleteView.as_view(), name='materials-delete'),
    path('<int:pk>/comment/', add_material_comment, name='materials-comment-add'),
    path('comment/<int:pk>/like/', toggle_material_comment_like, name='materials-comment-like'),
)