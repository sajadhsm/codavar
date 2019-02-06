from django.contrib import admin

from .models import Contest, Problem, Submission

admin.site.register(Contest)
admin.site.register(Problem)
admin.site.register(Submission)