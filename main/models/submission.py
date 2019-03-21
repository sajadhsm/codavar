import secrets
from zipfile import ZipFile

from .problem import Problem

from django.db import models
from django.contrib.auth import get_user_model

def generate_filename(instance, filename):
    # Makes it a little harder to guess the file location for end user
    # by using random secret token
    # TODO: But it's still possible for every one to download the file
    # if they find the actual file URL
    # Maybe try: https://github.com/edoburu/django-private-storage
    return "submissions/{}/{}".format(secrets.token_urlsafe(10), filename)

class Submission(models.Model):
    upload_date = models.DateTimeField(auto_now_add=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    zip_file = models.FileField(upload_to=generate_filename)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    judge_score = models.IntegerField(null=True)
    is_final = models.BooleanField(default=False)

    def __str__(self):
        return "{} by {} at {}".format(self.problem.title, self.user.email, self.upload_date)
    
    def set_as_final(self):
        '''
        Set only one instance of current problem user submission as final
        '''
        Submission.objects.filter(
            user=self.user,
            problem=self.problem,
            is_final=True
        ).update(is_final=False)
        self.is_final = True
        self.save()
    
    def contest_start_timedelta(self):
        return self.upload_date - self.problem.contest.start_date

    def extract(self):
        with ZipFile(self.zip_file.path, 'r') as zip: 
            # Extract the zip content to same name sibiling directory
            zip.extractall(self.zip_file.path[:-4])