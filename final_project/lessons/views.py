from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from final_project.lessons.forms import CreateLessonForm, LessonSearchForm
from final_project.lessons.models import Lesson


class CreateLessonView(views.CreateView):
    model = Lesson
    form_class = CreateLessonForm
    template_name = 'lessons/lesson-create.html'
    success_url = reverse_lazy('lesson-index')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        form.instance.teacher = self.request.user

        return form


class LessonIndexView(views.ListView):
    model = Lesson
    template_name = 'lessons/lesson-index.html'
    paginate_by = 4

    def get_queryset(self):
        search_form = LessonSearchForm(self.request.GET)
        search_pattern = None
        if search_form.is_valid():
            search_pattern = search_form.cleaned_data['lesson_title']

        lessons = Lesson.objects.all()

        if search_pattern:
            lessons = lessons.filter(title__icontains=search_pattern)

        return lessons

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_form'] = LessonSearchForm(self.request.GET)

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
    fields = ('title', 'price')

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


class OwnLessonView(views.ListView):
    model = Lesson
    template_name = 'lessons/lesson-index.html'
    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        queryset = Lesson.objects \
            .filter(teacher=self.request.user) \
            .all()

        return queryset

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, *kwargs)

        if request.user.user_type == 'student':
            return redirect('index')

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_form'] = LessonSearchForm(self.request.GET)

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
