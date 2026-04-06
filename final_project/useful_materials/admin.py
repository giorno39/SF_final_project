from django.contrib import admin

from final_project.useful_materials.models import Materials, MaterialComment


class MaterialCommentInline(admin.TabularInline):
    model = MaterialComment
    extra = 0
    readonly_fields = ('author', 'created_at')


@admin.register(Materials)
class MaterialsAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_specializations', 'uploaded_by')
    list_display_links = ('title', 'uploaded_by')
    ordering = ('title',)
    search_fields = ('title', 'specializations__name', 'uploaded_by__username', 'uploaded_by__email')
    filter_horizontal = ('specializations',)
    inlines = [MaterialCommentInline]

    fieldsets = (
        (
            'Main info',
            {
                'fields': (
                    'title',
                    'specializations',
                ),
            },
        ),
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

    @admin.display(description='Specializations')
    def get_specializations(self, obj):
        return ', '.join(obj.specializations.values_list('name', flat=True))


@admin.register(MaterialComment)
class MaterialCommentAdmin(admin.ModelAdmin):
    list_display = ('material', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('material__title', 'author__username', 'author__email', 'content')
    ordering = ('-created_at',)