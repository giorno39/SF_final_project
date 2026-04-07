from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Conversation(models.Model):
    participants = models.ManyToManyField(
        UserModel,
        related_name='conversations',
    )
    term_paper = models.ForeignKey(
        'term_papers.TermPaper',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversations',
    )
    lesson = models.ForeignKey(
        'lessons.Lesson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversations',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def last_message(self):
        return self.messages.order_by('-timestamp').first()

    def unread_count_for(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()

    def other_participant(self, user):
        return self.participants.exclude(pk=user.pk).first()

    def __str__(self):
        return f'Conversation #{self.pk}'


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    sender = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_messages',
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        sender_name = self.sender.get_full_name() if self.sender else 'System'
        return f'{sender_name}: {self.content[:40]}'