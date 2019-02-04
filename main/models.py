from django.db import models
from django.contrib.auth.models import User

from zipfile import ZipFile

class Contest(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name

class Problem(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

def generate_filename(instance, filename):
    return "zipfiles/{}/{}".format(instance.user.username, filename)

class Submission(models.Model):
    upload_date = models.DateTimeField(auto_now_add=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    zip_file = models.FileField(upload_to=generate_filename)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    judge_score = models.IntegerField(null=True)

    def __str__(self):
        return "{} by {} at {}".format(self.problem.title, self.user.username, self.upload_date)
    
    def extract(self):
        with ZipFile(self.zip_file.path, 'r') as zip: 
            # Extract the zip content to same name sibiling directory
            zip.extractall(self.zip_file.path[:-4])