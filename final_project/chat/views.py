from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Max
from django.shortcuts import get_object_or_404, redirect
from django.views import View, generic as views

from final_project.chat.models import Conversation, Message
from final_project.lessons.models import Lesson


class InboxView(LoginRequiredMixin, views.ListView):
    template_name = 'chat/inbox.html'
    context_object_name = 'conversations'

    def get_queryset(self):
        return (
            Conversation.objects
            .filter(participants=self.request.user)
            .annotate(latest_message_time=Max('messages__timestamp'))
            .order_by('-latest_message_time')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversations_data = []
        for convo in context['conversations']:
            conversations_data.append({
                'conversation': convo,
                'other_user': convo.other_participant(self.request.user),
                'last_message': convo.last_message,
                'unread_count': convo.unread_count_for(self.request.user),
            })
        context['conversations_data'] = conversations_data
        return context


class ConversationView(LoginRequiredMixin, views.DetailView):
    model = Conversation
    template_name = 'chat/conversation.html'
    context_object_name = 'conversation'

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat_messages'] = self.object.messages.select_related('sender').all()
        context['other_user'] = self.object.other_participant(self.request.user)

        Message.objects.filter(
            conversation=self.object,
            is_read=False,
        ).exclude(sender=self.request.user).update(is_read=True)

        return context


class StartLessonConversationView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        lesson = get_object_or_404(Lesson.objects.select_related('teacher'), pk=pk)
        other_user = lesson.teacher

        if request.user == other_user:
            return redirect('lesson-details', pk=lesson.pk)

        conversation = (
            Conversation.objects
            .filter(lesson=lesson, participants=request.user)
            .filter(participants=other_user)
            .annotate(num_participants=Count('participants'))
            .filter(num_participants=2)
            .first()
        )

        if not conversation:
            conversation = Conversation.objects.create(lesson=lesson)
            conversation.participants.add(request.user, other_user)

        return redirect('chat-conversation', pk=conversation.pk)