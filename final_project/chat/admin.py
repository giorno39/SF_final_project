from django.contrib import admin

from final_project.chat.models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'term_paper', 'created_at')
    filter_horizontal = ('participants',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'short_content', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')

    @staticmethod
    def short_content(obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
