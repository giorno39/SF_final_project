import rangefilter.filters
from django.contrib import admin

from final_project.lessons.models import Lesson


# Register your models here.
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_filter = [
            (
                'price', rangefilter.filters.NumericRangeFilterBuilder()
            )
        ]

    list_display = ('title', 'subject', 'price', 'teacher',)
    list_display_links = ('title', 'subject', 'price', 'teacher', )
    ordering = ('price', 'subject',)

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
            'Price info',
            {
                'fields': (
                    'price',
                ),
            },
        ),
        (
            'Teacher info',
            {
                'fields': (
                    'teacher',
                ),
            },
        ),
    )

