from django.contrib import admin
from django.db.models import Count

from .models.front_end_contest import FrontEndContest, FrontEndContestParticipation

@admin.register(FrontEndContest)
class FrontEndContestAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'start_date',
        'end_date',
        'duration',
        'problems_count',
        'participants_count',
        'is_public'
    ]
    list_filter = ['is_public']
    search_fields = ['name']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _problems_count=Count("problems", distinct=True),
            _participants_count=Count("participants", distinct=True),
        )
        return queryset
    
    def problems_count(self, obj):
        return obj._problems_count
    problems_count.admin_order_field = '_problems_count'
    
    def participants_count(self, obj):
        return obj._participants_count
    participants_count.admin_order_field = '_participants_count'

@admin.register(FrontEndContestParticipation)
class FrontEndContestParticipationAdmin(admin.ModelAdmin):
    readonly_fields = ('reg_date',)
    
    list_display = ['participant', 'contest', 'reg_date']
    list_filter = ['contest', 'reg_date']
    search_fields = ['contest', 'participant']