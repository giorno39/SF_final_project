import rangefilter.filters
from django.contrib import admin

from final_project.lessons.models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_filter = [
        (
            'price', rangefilter.filters.NumericRangeFilterBuilder()
        )
    ]

    list_display = ('title', 'price', 'teacher',)
    list_display_links = ('title', 'price', 'teacher',)
    ordering = ('price', 'title',)
    filter_horizontal = ('specializations',)

    fieldsets = (
        (
            'Main Info',
            {
                'fields': (
                    'title',
                    'specializations',
                    'cover_image',
                ),
            }
        ),
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