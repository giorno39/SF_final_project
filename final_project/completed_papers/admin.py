from django.contrib import admin
from final_project.completed_papers.models import CompletedPaper


@admin.register(CompletedPaper)
class CompletedPaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'university', 'has_author']
    list_display_links = ['has_author', 'university', 'title']
    ordering = ['university']
    list_filter = ['university']

    fieldsets = (
        (
            'Main Info',
            {
                'fields': (
                    'title',
                ),
            }),
        (
            'University',
            {
                'fields': (
                    'university',
                ),
            },
        ),
        (
            'Content',
            {
                'fields': (
                    'content',
                ),
            },
        ),
        (
            'Teacher info',
            {
                'fields': (
                    'completed_by',
                ),
            },
        ),
    )

    @admin.display(description='AUTHOR', ordering='completed_by', empty_value='-')
    def has_author(self, obj):
        if not obj.completed_by:
            return '-'
        return obj.completed_by