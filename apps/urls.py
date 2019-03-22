from django.urls import include, path

from .contest.views import index as landing_view

from .contest import urls as contest_urls
from .submission import urls as submission_urls
from .accounts import urls as accounts_urls

urlpatterns = [
    path('', landing_view, name='index'),
    path('contest/', include(contest_urls)),
    path('submission/', include(submission_urls)),
    path('accounts/', include(accounts_urls)),
]
