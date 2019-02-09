from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import Contest

def contest_has_started(function):
    def wrap(request, *args, **kwargs):
        contest = get_object_or_404(Contest, pk=kwargs['contest_pk'])

        if contest.has_started():
            return function(request, *args, **kwargs)
        else:
            raise Http404
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap