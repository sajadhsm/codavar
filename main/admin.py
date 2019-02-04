from django.contrib import admin

from .models import Contest, Problem

admin.site.register(Contest)
admin.site.register(Problem)