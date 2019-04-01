from django.shortcuts import render

from apps.contest.models import FrontEndContest

def index(request):
    contests = FrontEndContest.objects.all()
    return render(request, 'pages/index.html', {'contests': contests})