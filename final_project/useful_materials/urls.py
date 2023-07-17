from django.urls import path

from final_project.useful_materials.views import MaterialsIndexView, MaterialCreateView, MaterialDetailsView, \
    download_completed_paper, MaterialEditView, MaterialDeleteView

urlpatterns = (
    path('', MaterialsIndexView.as_view(), name='materials-index'),
    path('add/', MaterialCreateView.as_view(), name='materials-add'),
    path('details/<int:pk>', MaterialDetailsView.as_view(), name='materials-details'),
    path('download-file/<int:pk>', download_completed_paper, name='materials-download'),
    path('edit/<int:pk>', MaterialEditView.as_view(), name='materials-edit'),
    path('delete/<int:pk>', MaterialDeleteView.as_view(), name='materials-delete'),

)