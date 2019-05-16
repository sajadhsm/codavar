from django.contrib import admin

from .models.front_end_submission import FrontEndSubmission
from apps.contest.tasks import run_selenium_test

@admin.register(FrontEndSubmission)
class FrontEndSubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ('upload_date',)
    
    list_display = ['user', 'problem', 'upload_date', 'status']
    list_filter = ['status', 'user', 'problem']
    search_fields = ['user__email', 'problem__title']

    actions = ['rejudge_submissions']

    def rejudge_submissions(self, request, queryset):
        for submission in queryset:
            run_selenium_test.delay(submission.pk)
        sub_count = queryset.count()
        msg_bit = '1 submission is' if sub_count == 1 else f'{sub_count} submissions are'
        self.message_user(request, f'{msg_bit} being re-judged. (Reload the page after a few seconds)')
    rejudge_submissions.short_description = 'Re-judge selected submissions'