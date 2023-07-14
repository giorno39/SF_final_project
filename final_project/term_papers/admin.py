from django.contrib import admin

from final_project.term_papers.models import TermPaper


# Register your models here.

@admin.register(TermPaper)
class TermPaperAdmin(admin.ModelAdmin):
    pass
