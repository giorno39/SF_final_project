from django.contrib import admin

from final_project.useful_materials.models import Materials


# Register your models here.
@admin.register(Materials)
class PetAdmin(admin.ModelAdmin):
    list_display = ('title', 'field', 'uploaded_by',)
    list_display_links = ('title', 'field', 'uploaded_by')
    ordering = ('field', 'title')

    fieldsets = (
        (
            'Main info',
            {
                'fields': (
                    'title',
                    'field',
                ),
            }),
        (
            'Content info',
            {
                'fields': (
                    'content',
                    'references',
                ),
            },
        ),
        (
            'Author',
            {
                'fields': (
                    'uploaded_by',
                ),
            },
        ),
    )
