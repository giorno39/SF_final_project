import rangefilter.filters
from django.contrib import admin

from final_project.term_papers.models import TermPaper


@admin.register(TermPaper)
class TermPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_specializations', 'price_cap', 'user', 'taken_by', 'death_line')
    list_display_links = ('title', 'price_cap')

    list_filter = [
        (
            'price_cap', rangefilter.filters.NumericRangeFilterBuilder()
        ),
        (
            'death_line', rangefilter.filters.DateRangeFilterBuilder()
        ),
        'specializations',
    ]

    ordering = ['death_line', 'price_cap']

    fieldsets = (
        (
            'Main info',
            {
                'fields': (
                    'title',
                    'specializations',
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

    def get_specializations(self, obj):
        return ", ".join(spec.name for spec in obj.specializations.all())

    get_specializations.short_description = 'Specializations'