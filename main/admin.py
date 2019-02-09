from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Contest, Problem, Submission

class ProblemAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'

admin.site.register(Contest)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Submission)