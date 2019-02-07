from django.db import models
from django.contrib.auth.models import User

from zipfile import ZipFile

class Contest(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    users = models.ManyToManyField(User, related_name="contests", related_query_name="users", blank=True)

    def __str__(self):
        return self.name

class Problem(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    # used as module path for __import__
    selenium_script_as_module_string = models.CharField(max_length=500)

    def __str__(self):
        return self.title
    
    def run_selenium_script(self, sub_dir_path):
        _temp = __import__(
            self.selenium_script_as_module_string,
            globals=globals(),
            fromlist=['selenium_test'],
            level=1)
        selenium_test = _temp.selenium_test
        return selenium_test(sub_dir_path)

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
    
    def extract(self):
        with ZipFile(self.zip_file.path, 'r') as zip: 
            # Extract the zip content to same name sibiling directory
            zip.extractall(self.zip_file.path[:-4])