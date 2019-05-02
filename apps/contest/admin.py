from django.contrib import admin

from .models.front_end_contest import FrontEndContest, FrontEndContestParticipation

@admin.register(FrontEndContestParticipation)
class FrontEndContestParticipationAdmin(admin.ModelAdmin):
    readonly_fields = ('reg_date',)
    
    list_display = ['participant', 'contest', 'reg_date']
    list_filter = ['contest', 'reg_date']
    search_fields = ['contest', 'participant']

admin.site.register(FrontEndContest)