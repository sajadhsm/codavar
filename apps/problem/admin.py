from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Problem

class ProblemAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'

admin.site.register(Problem, ProblemAdmin)