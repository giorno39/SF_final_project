from datetime import datetime, date
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic as views
import os

from final_project import settings
from final_project.accounts.models import TeacherProfile
from final_project.completed_papers.models import CompletedPaper
from final_project.core.funcs import get_user_by_id
from final_project.chat.models import Conversation, Message
from final_project.term_papers.forms import TermPaperCreateForm, TermPaperSearchForm
from final_project.term_papers.models import TermPaper, TermPaperRequest
from final_project.term_papers.services.teacher_recommendation import rank_teachers_with_ai

UserModel = get_user_model()

def get_or_create_teacher_profile(user):
    teacher_profile, _ = TeacherProfile.objects.get_or_create(user=user)
    return teacher_profile


def get_unassign_penalty_points(term_paper):
    today = timezone.now().date()
    days_until_deadline = (term_paper.death_line - today).days

    if days_until_deadline < 0:
        return 4
    if days_until_deadline <= 7:
        return 3
    if days_until_deadline <= 14:
        return 2
    return 1


def is_late_unassignment(term_paper):
    today = timezone.now().date()
    days_until_deadline = (term_paper.death_line - today).days
    return days_until_deadline <= 7


def get_completion_reward_points(term_paper):
    today = timezone.now().date()
    days_before_deadline = (term_paper.death_line - today).days

    if days_before_deadline >= 14:
        return 3
    if days_before_deadline >= 7:
        return 2
    if days_before_deadline >= 0:
        return 1
    return 0

class TermPaperIndexView(views.ListView):
    model = TermPaper
    template_name = 'term-papers/term-paper-index.html'
    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        search_form = TermPaperSearchForm(self.request.GET)
        search_pattern = None
        if search_form.is_valid():
            search_pattern = search_form.cleaned_data['paper_title']

        queryset = (
            TermPaper.objects
            .filter(
                taken_by=None,
                completed=False,
                death_line__gt=datetime.today(),
            )
            .exclude(
                requests__status=TermPaperRequest.StatusChoices.PENDING,
            )
            .distinct()
        )

        if search_pattern:
            queryset = queryset.filter(title__icontains=search_pattern)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_form'] = TermPaperSearchForm(self.request.GET)

        return context


class TermPaperDetailsView(views.DetailView):
    model = TermPaper
    template_name = 'term-papers/term-paper-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pending_request = self.object.requests.filter(
            status=TermPaperRequest.StatusChoices.PENDING,
        ).exists()

        declined_request = self.object.requests.filter(
            status=TermPaperRequest.StatusChoices.DECLINED,
        ).exists()

        context['is_owner'] = self.request.user.pk == self.object.user_id
        context['is_taken'] = self.object.taken_by
        context['has_pending_request'] = pending_request
        context['has_declined_request'] = declined_request

        return context


class TermPaperCreateView(views.CreateView):
    model = TermPaper
    form_class = TermPaperCreateForm
    template_name = 'term-papers/term-paper-add.html'

    def get_success_url(self):
        return reverse_lazy('term-paper-request-teacher', kwargs={
            'pk': self.object.pk,
        })

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.user = self.request.user

        return form

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        c_user = get_user_by_id(self.request.user.pk)

        if c_user.user_type == 'teacher':
            return redirect('index')

        return result


class TermPaperEditView(views.UpdateView):
    model = TermPaper
    fields = ('title', 'death_line', 'price_cap','description')
    template_name = 'term-papers/term-paper-edit.html'

    def get_success_url(self):
        return reverse_lazy('term-paper-details', kwargs={
            'pk': self.object.pk,
        })

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        if self.request.user != self.object.user:
            result = reverse_lazy('term-paper-details', kwargs={
                'pk': self.object.pk,
            })

            return redirect(result)

        return result


class TermPaperDeleteView(views.DeleteView):
    model = TermPaper
    template_name = 'term-papers/term-paper-delete.html'
    success_url = reverse_lazy('term-paper-index')

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)

        if self.request.user != self.object.user:
            result = reverse_lazy('term-paper-details', kwargs={
                'pk': self.object.pk,
            })

            return redirect(result)

        return result

    def post(self, *args, **kwargs):
        result = super().post(*args, **kwargs)

        path = os.path.join(settings.MEDIA_ROOT, str(self.object.content))
        os.remove(path)

        return result


def open_file(request, pk):
    term_paper = TermPaper.objects.filter(pk=pk).get()
    file_name = str(term_paper.content)
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response


@login_required
def take_term_paper(request, pk):
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer
    from final_project.chat.models import Conversation, Message

    c_user = get_user_by_id(request.user.pk)

    if c_user.user_type == 'student':
        return redirect('term-paper-details', pk=pk)

    term_paper = TermPaper.objects \
        .filter(pk=pk) \
        .get()

    has_pending_request = term_paper.requests.filter(
        status=TermPaperRequest.StatusChoices.PENDING,
    ).exists()

    if has_pending_request:
        messages.error(request, 'This term paper already has a pending teacher request.')
        return redirect('term-paper-details', pk=pk)

    term_paper.taken_by_id = request.user.pk
    term_paper.save()

    teacher_name = request.user.get_full_name() or request.user.username

    send_mail(
        subject=f'Your term paper "{term_paper.title}" has been taken!',
        message=(
            f'Hello {term_paper.user.get_full_name()},\n\n'
            f'Your term paper "{term_paper.title}" has been taken by '
            f'{teacher_name} ({request.user.email}).\n\n'
            f'You can now discuss the details in the chat.\n\n'
            f'Best regards,\nThe Platform Team'
        ),
        from_email=None,
        recipient_list=[term_paper.user.email],
        fail_silently=True,
    )

    conversation = Conversation.objects.create(term_paper=term_paper)
    conversation.participants.add(request.user, term_paper.user)

    auto_text = f"Hi! I've taken your paper \"{term_paper.title}\". Let's discuss the details!"

    message = Message.objects.create(
        conversation=conversation,
        sender=request.user,
        content=auto_text,
    )

    student = term_paper.user
    unread_count = Message.objects.filter(
        conversation__participants=student,
        is_read=False,
    ).exclude(sender=student).count()

    try:
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f'chat_{conversation.pk}',
            {
                'type': 'chat_message',
                'sender_id': request.user.pk,
                'sender_name': teacher_name,
                'content': auto_text,
                'timestamp': message.timestamp.strftime('%H:%M'),
            }
        )

        async_to_sync(channel_layer.group_send)(
            f'notifications_{student.pk}',
            {
                'type': 'new_message',
                'conversation_id': conversation.pk,
                'sender_name': teacher_name,
                'preview': auto_text[:80],
                'unread_count': unread_count,
            },
        )
    except Exception:
        pass

    return redirect('term-paper-details', pk=pk)


class CompletePaper(views.UpdateView):
    model = TermPaper
    template_name = 'teacher/teacher-complete-paper.html'
    fields = ('content',)
    is_updatable = None

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['content'].widget = forms.FileInput()
        return form

    def get_success_url(self):
        return reverse_lazy('teacher-papers')

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)

        if self.is_updatable:
            self.object.completed = True

            completed_paper = CompletedPaper.objects.create(
                title=self.object.title,
                university=self.object.university,
                description=self.object.description,
                content=self.object.content,
                completed_by=self.object.taken_by,
            )
            completed_paper.specializations.set(self.object.specializations.all())

            teacher = self.object.taken_by
            if teacher:
                teacher_profile = get_or_create_teacher_profile(teacher)
                reward_points = get_completion_reward_points(self.object)

                if self.object.death_line >= timezone.now().date():
                    teacher_profile.completed_on_time_count += 1

                if (self.object.death_line - timezone.now().date()).days >= 7:
                    teacher_profile.completed_early_count += 1

                teacher_profile.increase_trust(reward_points)
                teacher_profile.save()

            self.object.save()

        return result

    def get(self, *args, **kwargs):
        result = super().get(*args, **kwargs)

        if self.request.user != self.object.taken_by:
            result = reverse_lazy('term-paper-details', kwargs={
                'pk': self.object.pk,
            })

            return redirect(result)

        return result

    def form_valid(self, form, *args, **kwargs):

        initial_data = self.get_object().__dict__.copy()

        cleaned_data = form.cleaned_data

        if initial_data['content'] == cleaned_data['content']:
            self.is_updatable = False
            return render(self.request, 'common/no-changes_detected.html')

        self.is_updatable = True

        return super().form_valid(form)

class TermPaperRequestTeacherListView(views.DetailView):
    model = TermPaper
    template_name = 'term-papers/term-paper-request-teacher.html'
    context_object_name = 'term_paper'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user != self.object.user:
            return redirect('term-paper-details', pk=self.object.pk)

        if self.object.taken_by:
            return redirect('term-paper-details', pk=self.object.pk)

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        requested_teacher_ids = set(
            self.object.requests.filter(
                status=TermPaperRequest.StatusChoices.PENDING,
            ).values_list('teacher_id', flat=True)
        )

        ai_recommendations = []
        ai_error = None

        try:
            ai_recommendations = rank_teachers_with_ai(
                term_paper=self.object,
                shortlist_size=8,
                result_size=3,
            )
        except Exception as exc:
            ai_error = str(exc)

        context['requested_teacher_ids'] = requested_teacher_ids
        context['ai_recommendations'] = ai_recommendations
        context['ai_error'] = ai_error

        return context

@login_required
def send_term_paper_request(request, pk, teacher_pk):
    term_paper = TermPaper.objects.filter(pk=pk).get()

    if request.user != term_paper.user:
        return redirect('term-paper-details', pk=pk)

    if term_paper.taken_by:
        messages.error(request, 'This term paper has already been taken.')
        return redirect('term-paper-details', pk=pk)

    teacher = UserModel.objects.filter(
        pk=teacher_pk,
        user_type='teacher',
    ).first()

    if not teacher:
        messages.error(request, 'Selected teacher does not exist.')
        return redirect('term-paper-request-teacher', pk=pk)

    existing_pending_request = TermPaperRequest.objects.filter(
        term_paper=term_paper,
        status=TermPaperRequest.StatusChoices.PENDING,
    ).exists()

    if existing_pending_request:
        messages.error(request, 'You already have a pending request for this term paper.')
        return redirect('term-paper-request-teacher', pk=pk)

    term_paper_request, created = TermPaperRequest.objects.get_or_create(
        term_paper=term_paper,
        teacher=teacher,
        defaults={
            'student': request.user,
            'status': TermPaperRequest.StatusChoices.PENDING,
        }
    )

    if not created:
        if term_paper_request.status == TermPaperRequest.StatusChoices.PENDING:
            messages.error(request, 'You have already requested this teacher.')
            return redirect('term-paper-request-teacher', pk=pk)

        term_paper_request.student = request.user
        term_paper_request.status = TermPaperRequest.StatusChoices.PENDING
        term_paper_request.responded_at = None
        term_paper_request.save()

    conversation = Conversation.objects.filter(
        term_paper=term_paper,
        participants=request.user,
    ).filter(
        participants=teacher,
    ).first()

    if not conversation:
        conversation = Conversation.objects.create(term_paper=term_paper)
        conversation.participants.add(request.user, teacher)

    auto_text = (
        f'Hello! I would like to request your help with my term paper '
        f'"{term_paper.title}". Please let me know whether you accept or decline.'
    )

    message = Message.objects.create(
        conversation=conversation,
        sender=request.user,
        content=auto_text,
    )

    unread_count = Message.objects.filter(
        conversation__participants=teacher,
        is_read=False,
    ).exclude(sender=teacher).count()

    try:
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f'chat_{conversation.pk}',
            {
                'type': 'chat_message',
                'sender_id': request.user.pk,
                'sender_name': request.user.get_full_name() or request.user.username,
                'content': auto_text,
                'timestamp': message.timestamp.strftime('%H:%M'),
            }
        )

        async_to_sync(channel_layer.group_send)(
            f'notifications_{teacher.pk}',
            {
                'type': 'new_message',
                'conversation_id': conversation.pk,
                'sender_name': request.user.get_full_name() or request.user.username,
                'preview': auto_text[:80],
                'unread_count': unread_count,
            },
        )
    except Exception:
        pass

    messages.success(request, 'Your request was sent successfully.')
    return redirect('chat-conversation', pk=conversation.pk)

class TeacherTermPaperRequestsListView(views.ListView):
    model = TermPaperRequest
    template_name = 'teacher/teacher-term-paper-requests.html'
    context_object_name = 'requests_list'

    def get_queryset(self):
        if self.request.user.user_type != 'teacher':
            return TermPaperRequest.objects.none()

        return (
            TermPaperRequest.objects
            .filter(
                teacher=self.request.user,
                status=TermPaperRequest.StatusChoices.PENDING,
                term_paper__taken_by__isnull=True,
            )
            .select_related('student', 'teacher', 'term_paper')
            .order_by('-created_at')
        )

@login_required
def accept_term_paper_request(request, request_pk):
    if request.user.user_type != 'teacher':
        return redirect('index')

    term_paper_request = (
        TermPaperRequest.objects
        .select_related('term_paper', 'student', 'teacher')
        .filter(pk=request_pk, teacher=request.user)
        .first()
    )

    if not term_paper_request:
        messages.error(request, 'Request not found.')
        return redirect('teacher-term-paper-requests')

    if term_paper_request.status != TermPaperRequest.StatusChoices.PENDING:
        messages.error(request, 'This request has already been processed.')
        return redirect('teacher-term-paper-requests')

    term_paper = term_paper_request.term_paper

    if term_paper.taken_by:
        term_paper_request.status = TermPaperRequest.StatusChoices.DECLINED
        term_paper_request.responded_at = timezone.now()
        term_paper_request.save()

        messages.error(request, 'This term paper has already been taken.')
        return redirect('teacher-term-paper-requests')

    term_paper.taken_by = request.user
    term_paper.save()

    term_paper_request.status = TermPaperRequest.StatusChoices.ACCEPTED
    term_paper_request.responded_at = timezone.now()
    term_paper_request.save()

    TermPaperRequest.objects.filter(
        term_paper=term_paper,
        status=TermPaperRequest.StatusChoices.PENDING,
    ).exclude(pk=term_paper_request.pk).update(
        status=TermPaperRequest.StatusChoices.DECLINED,
        responded_at=timezone.now(),
    )

    conversation = Conversation.objects.filter(
        term_paper=term_paper,
        participants=request.user,
    ).filter(
        participants=term_paper.user,
    ).first()

    if not conversation:
        conversation = Conversation.objects.create(term_paper=term_paper)
        conversation.participants.add(request.user, term_paper.user)

    auto_text = (
        f'{request.user.get_full_name() or request.user.username} accepted the request '
        f'for "{term_paper.title}".'
    )

    message = Message.objects.create(
        conversation=conversation,
        sender=request.user,
        content=auto_text,
    )

    student = term_paper.user
    unread_count = Message.objects.filter(
        conversation__participants=student,
        is_read=False,
    ).exclude(sender=student).count()

    try:
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f'chat_{conversation.pk}',
            {
                'type': 'chat_message',
                'sender_id': request.user.pk,
                'sender_name': request.user.get_full_name() or request.user.username,
                'content': auto_text,
                'timestamp': message.timestamp.strftime('%H:%M'),
            }
        )

        async_to_sync(channel_layer.group_send)(
            f'notifications_{student.pk}',
            {
                'type': 'new_message',
                'conversation_id': conversation.pk,
                'sender_name': request.user.get_full_name() or request.user.username,
                'preview': auto_text[:80],
                'unread_count': unread_count,
            },
        )
    except Exception:
        pass

    messages.success(request, 'You accepted the request.')
    return redirect('chat-conversation', pk=conversation.pk)


@login_required
def decline_term_paper_request(request, request_pk):
    if request.user.user_type != 'teacher':
        return redirect('index')

    term_paper_request = (
        TermPaperRequest.objects
        .select_related('term_paper', 'student', 'teacher')
        .filter(pk=request_pk, teacher=request.user)
        .first()
    )

    if not term_paper_request:
        messages.error(request, 'Request not found.')
        return redirect('teacher-term-paper-requests')

    if term_paper_request.status != TermPaperRequest.StatusChoices.PENDING:
        messages.error(request, 'This request has already been processed.')
        return redirect('teacher-term-paper-requests')

    term_paper_request.status = TermPaperRequest.StatusChoices.DECLINED
    term_paper_request.responded_at = timezone.now()
    term_paper_request.save()

    conversation = Conversation.objects.filter(
        term_paper=term_paper_request.term_paper,
        participants=request.user,
    ).filter(
        participants=term_paper_request.student,
    ).first()

    if not conversation:
        conversation = Conversation.objects.create(term_paper=term_paper_request.term_paper)
        conversation.participants.add(request.user, term_paper_request.student)

    auto_text = (
        f'{request.user.get_full_name() or request.user.username} declined the request '
        f'for "{term_paper_request.term_paper.title}".'
    )

    message = Message.objects.create(
        conversation=conversation,
        sender=request.user,
        content=auto_text,
    )

    student = term_paper_request.student
    unread_count = Message.objects.filter(
        conversation__participants=student,
        is_read=False,
    ).exclude(sender=student).count()

    try:
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f'chat_{conversation.pk}',
            {
                'type': 'chat_message',
                'sender_id': request.user.pk,
                'sender_name': request.user.get_full_name() or request.user.username,
                'content': auto_text,
                'timestamp': message.timestamp.strftime('%H:%M'),
            }
        )

        async_to_sync(channel_layer.group_send)(
            f'notifications_{student.pk}',
            {
                'type': 'new_message',
                'conversation_id': conversation.pk,
                'sender_name': request.user.get_full_name() or request.user.username,
                'preview': auto_text[:80],
                'unread_count': unread_count,
            },
        )
    except Exception:
        pass

    messages.success(request, 'You declined the request.')
    return redirect('teacher-term-paper-requests')

@login_required
def unassign_term_paper(request, pk):
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer
    from final_project.chat.models import Conversation, Message

    if request.user.user_type != 'teacher':
        return redirect('index')

    term_paper = TermPaper.objects.filter(pk=pk).select_related('user', 'taken_by').first()

    if not term_paper:
        messages.error(request, 'Term paper not found.')
        return redirect('teacher-papers')

    if term_paper.taken_by != request.user:
        messages.error(request, 'You cannot unassigned this term paper.')
        return redirect('teacher-papers')

    if term_paper.completed:
        messages.error(request, 'Completed papers cannot be unassigned')
        return redirect('teacher-papers')

    teacher_profile = get_or_create_teacher_profile(request.user)
    penalty_points = get_unassign_penalty_points(term_paper)

    teacher_profile.unassignments_count += 1
    if is_late_unassignment(term_paper):
        teacher_profile.late_unassignments_count += 1

    teacher_profile.decrease_trust(penalty_points)
    teacher_profile.save()

    conversation = Conversation.objects.filter(
        term_paper=term_paper,
        participants=request.user,
    ).filter(
        participants=term_paper.user,
    ).first()

    if not conversation:
        conversation = Conversation.objects.create(term_paper=term_paper)
        conversation.participants.add(request.user, term_paper.user)

    auto_text = (
        f'{request.user.get_full_name() or request.user.username} is no longer '
        f'taking the term paper "{term_paper.title}". It is now available again.'
    )

    message = Message.objects.create(
        conversation=conversation,
        sender=request.user,
        content=auto_text,
    )

    student = term_paper.user
    unread_count = Message.objects.filter(
        conversation__participants=student,
        is_read=False,
    ).exclude(sender=student).count()

    try:
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f'chat_{conversation.pk}',
            {
                'type': 'chat_message',
                'sender_id': request.user.pk,
                'sender_name': request.user.get_full_name() or request.user.username,
                'content': auto_text,
                'timestamp': message.timestamp.strftime('%H:%M'),
            }
        )

        async_to_sync(channel_layer.group_send)(
            f'notifications_{student.pk}',
            {
                'type': 'new_message',
                'conversation_id': conversation.pk,
                'sender_name': request.user.get_full_name() or request.user.username,
                'preview': auto_text[:80],
                'unread_count': unread_count,
            },
        )
    except Exception:
        pass

    TermPaperRequest.objects.filter(
        term_paper=term_paper,
        teacher=request.user,
        status=TermPaperRequest.StatusChoices.ACCEPTED,
    ).update(
        status=TermPaperRequest.StatusChoices.CANCELED,
        responded_at=timezone.now(),
    )

    term_paper.taken_by = None
    term_paper.save()

    messages.success(request, 'You unassigned yourself from the term paper. It is now available again.')
    return redirect('teacher-papers')