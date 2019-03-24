from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models.front_end_problem import FrontEndProblem

class ProblemAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'

admin.site.register(FrontEndProblem, ProblemAdmin)