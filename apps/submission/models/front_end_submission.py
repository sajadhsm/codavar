import secrets
import os
from zipfile import ZipFile

from django.db import models
from django.contrib.auth import get_user_model

from apps.problem.models import FrontEndProblem
from apps.contest.models import FrontEndContest
from .abstract_base_submission import AbstractBaseSubmission

def generate_filename(instance, filename):
    # Makes it a little harder to guess the file location for end user
    # by using random secret token
    # TODO: But it's still possible for every one to download the file
    # if they find the actual file URL
    # Maybe try: https://github.com/edoburu/django-private-storage
    return f'submissions/fe/{secrets.token_urlsafe(10)}/{filename}'

class FrontEndSubmission(AbstractBaseSubmission):
    file = models.FileField(upload_to=generate_filename)
    problem = models.ForeignKey(
        FrontEndProblem,
        related_name='submissions',
        related_query_name='submission',
        on_delete=models.CASCADE
    )
    relative_score = models.FloatField(default=0)

    @property
    def judge_score(self):
        return int(self.relative_score * self.problem.score)
    
    def __str__(self):
        return f'{self.problem.title} by {self.user.email} at {self.upload_date}'

    def extract(self):
        """Extract the zip content to same name sibiling directory."""
        extract_path = self.get_file_extract_path()
        with ZipFile(self.file, 'r') as zip:
            for subfile in zip.namelist():
                zip.extract(subfile, path=extract_path)
    
    def get_file_extract_path(self):
        file_dir = os.path.splitext(self.file.path)[0]
        return file_dir + '_dir'


class FrontEndContestSubmission(FrontEndSubmission):
    contest = models.ForeignKey(FrontEndContest, on_delete=models.CASCADE)
    is_final = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.problem.title}({self.contest.name}) by {self.user.email} at {self.upload_date}'
    
    def set_as_final(self):
        '''
        Set only one instance of current problem user submission as final
        '''
        FrontEndContestSubmission.objects.filter(
            user=self.user,
            contest=self.contest,
            problem=self.problem,
            is_final=True
        ).update(is_final=False)
        self.is_final = True
        self.save()
    
    def contest_start_timedelta(self):
        return self.upload_date - self.contest.start_date