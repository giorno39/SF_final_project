from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
import os

from final_project import settings
from final_project.useful_materials.forms import MaterialCreateForm, MaterialSearchForm
from final_project.useful_materials.models import Materials


# Create your views here.


class MaterialsIndexView(views.ListView):
    model = Materials
    template_name = 'useful_material/materials-index.html'

    def get_queryset(self):
        search_form = MaterialSearchForm(self.request.GET)
        search_pattern = None
        if search_form.is_valid():
            search_pattern = search_form.cleaned_data['material_title']

        materials = Materials.objects.all()

        if search_pattern:
            materials = materials.filter(title__icontains=search_pattern)

        return materials

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_form'] = MaterialSearchForm(self.request.GET)

        return context


class MaterialCreateView(LoginRequiredMixin, views.CreateView):
    model = Materials
    form_class = MaterialCreateForm
    template_name = 'useful_material/materials-add.html'
    success_url = reverse_lazy('materials-index')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.uploaded_by = self.request.user

        return form


class MaterialDetailsView(views.DetailView):
    model = Materials
    template_name = 'useful_material/materials-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_owner'] = self.request.user == self.object.uploaded_by

        return context


class MaterialEditView(views.UpdateView):
    model = Materials
    fields = ('content', 'references',)
    template_name = 'useful_material/materials-edit.html'

    def get_success_url(self):
        return reverse_lazy('materials-details', kwargs={
            'pk': self.object.pk
        })

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)

        if request.user != self.object.uploaded_by:
            result = reverse_lazy('materials-details', kwargs={
                'pk': self.object.pk
            })
            return redirect(result)

        return result


class MaterialDeleteView(views.DeleteView):
    model = Materials
    template_name = 'useful_material/materials-delete.html'
    success_url = reverse_lazy('materials-index')

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)

        if request.user != self.object.uploaded_by:
            result = reverse_lazy('materials-details', kwargs={
                'pk': self.object.pk
            })
            return redirect(result)

        return result


def download_completed_paper(request, pk):
    term_paper = Materials.objects.filter(pk=pk).get()
    file_name = str(term_paper.content)
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response
