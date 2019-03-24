from django.contrib import admin

from .models.front_end_contest import FrontEndContest, FrontEndContestParticipation

admin.site.register(FrontEndContest)
admin.site.register(FrontEndContestParticipation)