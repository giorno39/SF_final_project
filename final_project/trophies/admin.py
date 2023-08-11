import rangefilter.filters
from django.contrib import admin

from final_project.trophies.models import Trophy


# Register your models here.
@admin.register(Trophy)
class TrophyAdmin(admin.ModelAdmin):
    list_display = ('project', 'rate', 'obtained_at', 'earned_by',)
    list_display_links = ('project', 'rate', 'obtained_at', 'earned_by')
    list_filter = [
        (
            'rate', rangefilter.filters.NumericRangeFilterBuilder()
        ),
        (
            'obtained_at', rangefilter.filters.DateRangeFilterBuilder()
        )
    ]

    ordering = ('obtained_at', 'rate')

    fieldsets = (
        (
            'Main info',
            {
                'fields': (
                    'rate',
                    'project',
                ),
            }
        ),

        (
            'Teacher',
            {
                'fields': (
                    'completed_by',
                ),
            },
        ),
    )

    @admin.display(empty_value='-')
    def earned_by(self, obj):
        return obj.completed_by

    earned_by.short_description = 'earned by'
