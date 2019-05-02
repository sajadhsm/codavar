from django.contrib import admin

from .models.front_end_submission import FrontEndSubmission

@admin.register(FrontEndSubmission)
class FrontEndSubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ('upload_date',)
    
    list_display = ['user', 'problem', 'upload_date', 'status']
    list_filter = ['status', 'user', 'problem']
    search_fields = ['user__email', 'problem__title']