from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models.front_end_problem import FrontEndProblem

@admin.register(FrontEndProblem)
class FrontEndProblemAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'

    list_display = ['title', 'score']
    search_fields = ['title']