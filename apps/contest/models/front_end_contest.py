from django.db import models
from django.contrib.auth import get_user_model

from .abstract_base_contest import AbstractBaseContest
from apps.problem.models import FrontEndProblem

class FrontEndContest(AbstractBaseContest):
    participants = models.ManyToManyField(
        get_user_model(),
        through='FrontEndContestParticipation',
        related_name='front_end_contests',
        related_query_name='front_end_contest'
    )
    problems = models.ManyToManyField(
        FrontEndProblem,
        related_name='contests',
        related_query_name='contest',
        blank=True
    )

class FrontEndContestParticipation(models.Model):
    participant = models.ForeignKey(
        get_user_model(),
        related_name='front_end_contest_participations',
        related_query_name='front_end_contest_participation',
        on_delete=models.CASCADE
    )
    contest = models.ForeignKey(
        FrontEndContest,
        related_name='participations',
        related_query_name='participation',
        on_delete=models.CASCADE
    )
    reg_date = models.DateTimeField(auto_now_add=True)