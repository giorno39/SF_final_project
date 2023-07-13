from django.urls import path

from final_project.common.views import index

urlpatterns = (
    path('', index, name='index'),
)
