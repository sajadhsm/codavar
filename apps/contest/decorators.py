from functools import wraps

from django.shortcuts import get_object_or_404
from django.http import Http404

def check_contest_access(ContestModel):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            contest = get_object_or_404(ContestModel, pk=kwargs['contest_pk'])
            if contest.is_public and contest.has_started:
                return view_func(request, *args, **kwargs)
            raise Http404 
        return _wrapped_view
    return decorator