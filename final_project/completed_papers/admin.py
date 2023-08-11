from django.contrib import admin

from final_project.completed_papers.models import CompletedPaper


# Register your models here.
@admin.register(CompletedPaper)
class CompletedPaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'university', 'has_author']
    list_display_links = ['subject', 'has_author', 'university', 'title', ]
    ordering = ['university', 'subject', ]
    list_filter = ['university', ]

    fieldsets = (
        (
            'Main Info',
            {
                'fields': (
                    'title',
                    'subject',
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

    admin.display(empty_value='-')

    def has_author(self, obj):
        if not obj.completed_by:
            return '-'
        return obj.completed_by

    has_author.short_description = 'AUTHOR'
    has_author.admin_order_field = 'completed_by'
