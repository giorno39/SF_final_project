from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.views import generic as views

from final_project.chat.models import Conversation, Message


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
