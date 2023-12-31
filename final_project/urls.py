"""
URL configuration for final_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls,),
    path('', include('final_project.common.urls')),
    path('accounts/', include('final_project.accounts.urls')),
    path('term-paper/', include('final_project.term_papers.urls')),
    path('trophy/', include('final_project.trophies.urls')),
    path('lesson/', include('final_project.lessons.urls')),
    path('completed-papers/', include('final_project.completed_papers.urls')),
    path('useful-materials/', include('final_project.useful_materials.urls')),
    path('custom-admin/', include('final_project.administration.urls'))

]
