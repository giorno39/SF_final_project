import os
from os import path
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import FileResponse
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Count, Exists, OuterRef
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic as views
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from final_project import settings
from final_project.useful_materials.forms import (
    MaterialCreateForm,
    MaterialEditForm,
    MaterialSearchForm,
    MaterialCommentForm,
)
from final_project.useful_materials.models import Materials, MaterialComment, MaterialCommentVote


class MaterialsIndexView(views.ListView):
    model = Materials
    template_name = 'useful_material/materials-index.html'
    paginate_by = 4

    def get_queryset(self):
        search_form = MaterialSearchForm(self.request.GET)
        materials = Materials.objects.all().prefetch_related('specializations')

        if search_form.is_valid():
            search_pattern = search_form.cleaned_data['material_title']
            specialization = search_form.cleaned_data['specialization']

            if search_pattern:
                materials = materials.filter(title__icontains=search_pattern)

            if specialization:
                materials = materials.filter(specializations=specialization)

        return materials.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = MaterialSearchForm(self.request.GET)
        return context


class MaterialCreateView(LoginRequiredMixin, views.CreateView):
    model = Materials
    form_class = MaterialCreateForm
    template_name = 'useful_material/materials-add.html'
    success_url = reverse_lazy('materials-index')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)


class MaterialDetailsView(views.DetailView):
    model = Materials
    template_name = 'useful_material/materials-details.html'
    comments_paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()
        last_24h = now - timedelta(hours=24)

        comments_last_24h = 0
        remaining_comments = 3

        if self.request.user.is_authenticated:
            comments_last_24h = MaterialComment.objects.filter(
                material=self.object,
                author=self.request.user,
                created_at__gte=last_24h,
            ).count()
            remaining_comments = max(0, 3 - comments_last_24h)

        comments_qs = self.object.comments.select_related('author').annotate(
            likes_count=Count('votes', distinct=True),
            user_has_liked=Exists(
                MaterialCommentVote.objects.filter(
                    comment=OuterRef('pk'),
                    user=self.request.user,
                )
            ) if self.request.user.is_authenticated else False,
        ).order_by('-likes_count', '-created_at')
        paginator = Paginator(comments_qs, self.comments_paginate_by)
        page_number = self.request.GET.get('page')
        comments_page = paginator.get_page(page_number)

        context['is_owner'] = self.request.user == self.object.uploaded_by
        context['comment_form'] = MaterialCommentForm()
        context['comments'] = comments_page
        context['comments_last_24h'] = comments_last_24h
        context['remaining_comments'] = remaining_comments
        context['comments_page_obj'] = comments_page
        context['comments_is_paginated'] = comments_page.paginator.num_pages > 1

        return context


class MaterialEditView(LoginRequiredMixin, views.UpdateView):
    model = Materials
    form_class = MaterialEditForm
    template_name = 'useful_material/materials-edit.html'

    def get_success_url(self):
        return reverse_lazy('materials-details', kwargs={
            'pk': self.object.pk
        })

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user != self.object.uploaded_by:
            return redirect('materials-details', pk=self.object.pk)

        return super().dispatch(request, *args, **kwargs)


class MaterialDeleteView(LoginRequiredMixin, views.DeleteView):
    model = Materials
    template_name = 'useful_material/materials-delete.html'
    success_url = reverse_lazy('materials-index')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user != self.object.uploaded_by:
            return redirect('materials-details', pk=self.object.pk)

        return super().dispatch(request, *args, **kwargs)


@login_required
def add_material_comment(request, pk):
    material = get_object_or_404(Materials, pk=pk)

    if request.method != 'POST':
        return redirect('materials-details', pk=material.pk)

    form = MaterialCommentForm(request.POST)

    if not form.is_valid():
        messages.error(request, _("Please enter a valid comment."))
        return redirect('materials-details', pk=material.pk)

    last_24h = timezone.now() - timedelta(hours=24)

    comments_count = MaterialComment.objects.filter(
        material=material,
        author=request.user,
        created_at__gte=last_24h,
    ).count()

    if comments_count >= 3:
        messages.error(request, _("You can post up to 3 comments per 24 hours for this material."))
        return redirect('materials-details', pk=material.pk)

    comment = form.save(commit=False)
    comment.material = material
    comment.author = request.user
    comment.save()

    messages.success(request, _("Your comment was posted successfully."))
    return redirect('materials-details', pk=material.pk)


def download_completed_paper(request, pk):
    material = Materials.objects.filter(pk=pk).get()
    file_name = str(material.content)
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response

@login_required
def toggle_material_comment_like(request, pk):
    comment = get_object_or_404(MaterialComment, pk=pk)

    if request.method != 'POST':
        return redirect('materials-details', pk=comment.material.pk)

    existing_vote = MaterialCommentVote.objects.filter(
        comment=comment,
        user=request.user,
    ).first()

    if existing_vote:
        existing_vote.delete()
        messages.success(request, _("Like removed."))
    else:
        MaterialCommentVote.objects.create(
            comment=comment,
            user=request.user,
        )
        messages.success(request, _("Comment liked."))

    page = request.POST.get('page')
    if page:
        return redirect(f"{reverse_lazy('materials-details', kwargs={'pk': comment.material.pk})}?page={page}")

    return redirect('materials-details', pk=comment.material.pk)