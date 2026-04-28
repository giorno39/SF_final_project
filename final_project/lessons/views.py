from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.utils.translation import gettext_lazy as _

from final_project.accounts.models import TypesOfUsers
from final_project.core.permissions_mixins import TeacherRequiredMixin
from final_project.lessons.forms import CreateLessonForm, LessonEditForm, LessonSearchForm
from final_project.lessons.models import Lesson

def _lesson_feed_querystring(request):
    q = request.GET.copy()
    q.pop('page', None)
    return q.urlencode()

class CreateLessonView(views.CreateView):
    model = Lesson
    form_class = CreateLessonForm
    template_name = 'lessons/lesson-create.html'
    success_url = reverse_lazy('lesson-index')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        form.instance.teacher = self.request.user

        teacher_profile = getattr(self.request.user, 'teacher_profile', None)
        if teacher_profile:
            form.fields['specializations'].queryset = teacher_profile.specializations.all()
        else:
            form.fields['specializations'].queryset = form.fields['specializations'].queryset.none()

        return form


class LessonIndexView(views.ListView):
    model = Lesson
    template_name = 'lessons/lesson-index.html'
    paginate_by = 6

    def get_queryset(self):
        search_form = LessonSearchForm(self.request.GET)
        search_pattern = None
        specialization = None

        lessons = Lesson.objects.all().prefetch_related('specializations')

        if search_form.is_valid():
            search_pattern = search_form.cleaned_data.get('lesson_title')
            specialization = search_form.cleaned_data.get('specialization')

        if search_pattern:
            lessons = lessons.filter(
                Q(title__icontains=search_pattern)
            )

        if specialization:
            lessons = lessons.filter(specializations=specialization)

        return lessons.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = LessonSearchForm(self.request.GET)
        context['lesson_feed_title'] = _('Lesson Discovery Feed')
        context['get_params'] = _lesson_feed_querystring(self.request)
        return context


class LessonDetailsView(views.DetailView):
    model = Lesson
    template_name = 'lessons/lesson-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.request.user == self.object.teacher
        return context


class LessonEditView(views.UpdateView):
    model = Lesson
    template_name = 'lessons/lesson-edit.html'
    form_class = LessonEditForm

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        teacher_profile = getattr(self.request.user, 'teacher_profile', None)
        if teacher_profile:
            form.fields['specializations'].queryset = teacher_profile.specializations.all()
        else:
            form.fields['specializations'].queryset = form.fields['specializations'].queryset.none()

        return form

    def get_success_url(self):
        return reverse_lazy('lesson-details', kwargs={
            'pk': self.object.pk,
        })

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)

        if self.request.user != self.object.teacher:
            result = reverse_lazy('lesson-details', kwargs={
                'pk': self.object.pk,
            })
            return redirect(result)

        return result


class OwnLessonView(TeacherRequiredMixin, views.ListView):
    model = Lesson
    template_name = 'lessons/lesson-index.html'
    paginate_by = 6

    def get_queryset(self, *args, **kwargs):
        search_form = LessonSearchForm(self.request.GET)
        search_pattern = None
        specialization = None

        queryset = Lesson.objects.filter(
            teacher=self.request.user
        ).prefetch_related('specializations')

        if search_form.is_valid():
            search_pattern = search_form.cleaned_data.get('lesson_title')
            specialization = search_form.cleaned_data.get('specialization')

        if search_pattern:
            queryset = queryset.filter(
                Q(title__icontains=search_pattern)
            )

        if specialization:
            queryset = queryset.filter(specializations=specialization)

        return queryset.distinct()

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)

        if request.user.user_type == TypesOfUsers.STUDENT:
            return redirect('index')

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_form'] = LessonSearchForm(self.request.GET)
        context['lesson_feed_title'] = _('My Lessons')
        context['get_params'] = _lesson_feed_querystring(self.request)

        return context


class LessonDeleteView(views.DeleteView):
    model = Lesson
    template_name = 'lessons/lesson-delete.html'
    success_url = reverse_lazy('own-lesson-index')

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)

        if self.request.user != self.object.teacher:
            result = reverse_lazy('lesson-details', kwargs={
                'pk': self.object.pk,
            })

            return redirect(result)

        return result