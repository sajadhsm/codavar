from zipfile import ZipFile

from .problem import Problem

from django.db import models
from django.contrib.auth.models import User

def generate_filename(instance, filename):
    return "zipfiles/{}/{}".format(instance.user.username, filename)

class Submission(models.Model):
    upload_date = models.DateTimeField(auto_now_add=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    zip_file = models.FileField(upload_to=generate_filename)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    judge_score = models.IntegerField(null=True)
    is_final = models.BooleanField(default=False)

    def __str__(self):
        return "{} by {} at {}".format(self.problem.title, self.user.username, self.upload_date)
    
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