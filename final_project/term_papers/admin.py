import rangefilter.filters
from django.contrib import admin

from final_project.term_papers.models import TermPaper


# Register your models here.

@admin.register(TermPaper)
class TermPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'price_cap', 'user', 'taken_by', 'death_line')
    list_display_links = ('title', 'price_cap')

    list_filter = [
            (
                'price_cap', rangefilter.filters.NumericRangeFilterBuilder()
            ),
            (
                'death_line', rangefilter.filters.DateRangeFilterBuilder()
            )
        ]

    ordering = ['death_line', 'price_cap',]

    fieldsets = (
        (
            'Main info',
            {
                'fields': (
                    'title',
                    'subject',
                    'university',
                    'death_line',
                ),
            }),
        (
            'Price info',
            {
                'fields': (
                    'price_cap',
                ),
            },
        ),
        (
            'Content info',
            {
                'fields': (
                    'description',
                    'content',
                ),
            },
        ),
        (
            'Other',
            {
                'fields': (
                    'user',
                    'taken_by',
                    'completed',
                    'rated',
                ),
            },
        ),
    )
