import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model

from final_project.chat.models import Conversation, Message

UserModel = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        self.user = self.scope['user']

        if self.user.is_anonymous:
            self.close()
            return

        try:
            conversation = Conversation.objects.get(pk=self.conversation_id)
            if not conversation.participants.filter(pk=self.user.pk).exists():
                self.close()
                return
        except Conversation.DoesNotExist:
            self.close()
            return

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()

    def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name,
            )

    def receive(self, text_data):
        data = json.loads(text_data)
        msg_type = data.get('type', '')

        if msg_type == 'chat_message':
            self._handle_chat_message(data)
        elif msg_type == 'mark_read':
            self._handle_mark_read()

    def _handle_chat_message(self, data):
        content = data.get('content', '').strip()
        if not content:
            return

        message = Message.objects.create(
            conversation_id=self.conversation_id,
            sender=self.user,
            content=content,
        )

        payload = {
            'type': 'chat_message',
            'message_id': message.pk,
            'sender_id': self.user.pk,
            'sender_name': self.user.get_full_name() or self.user.username,
            'content': content,
            'timestamp': message.timestamp.strftime('%b %d, %H:%M'),
        }

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            payload,
        )

        conversation = Conversation.objects.get(pk=self.conversation_id)
        other_user = conversation.other_participant(self.user)
        if other_user:
            unread_count = Message.objects.filter(
                conversation__participants=other_user,
                is_read=False,
            ).exclude(sender=other_user).count()

            async_to_sync(self.channel_layer.group_send)(
                f'notifications_{other_user.pk}',
                {
                    'type': 'new_message',
                    'conversation_id': self.conversation_id,
                    'sender_name': self.user.get_full_name() or self.user.username,
                    'preview': content[:80],
                    'unread_count': unread_count,
                },
            )

    def _handle_mark_read(self):
        Message.objects.filter(
            conversation_id=self.conversation_id,
            is_read=False,
        ).exclude(sender=self.user).update(is_read=True)

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']

        if self.user.is_anonymous:
            self.close()
            return

        self.group_name = f'notifications_{self.user.pk}'

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )
        self.accept()

        self._send_unread_count()

    def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name,
            )

    def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('type') == 'get_unread_count':
            self._send_unread_count()

    def _send_unread_count(self):
        count = Message.objects.filter(
            conversation__participants=self.user,
            is_read=False,
        ).exclude(sender=self.user).count()

        self.send(text_data=json.dumps({
            'type': 'unread_count',
            'count': count,
        }))

    def new_message(self, event):
        self.send(text_data=json.dumps(event))
