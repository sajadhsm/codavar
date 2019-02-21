import importlib

from .contest import Contest

from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage

upload_storage = FileSystemStorage(
    location=settings.SELENIUM_SCRIPT_UPLOAD_ROOT,
    base_url='/selenium_scripts')

def generate_filename(instance, filename):
    problem_name = instance.title.replace(" ", "_")
    file_name = filename.replace(" ", "_")
    return "{}__{}".format(problem_name, file_name)

class Problem(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=10)
    selenium_script = models.FileField(upload_to=generate_filename, storage=upload_storage)

    class Meta:
        ordering = ['score']

    def __str__(self):
        return self.title
    
    def selenium_script_as_module_string(self):
        return '.{}'.format(str(self.selenium_script).split('.py')[0])

    def run_selenium_script(self, sub_dir_path):
        script_module = importlib.import_module(
            self.selenium_script_as_module_string(),
            package=settings.SELENIUM_SCRIPT_IMPORT_MODULE_PACKAGE)
        selenium_test = script_module.selenium_test
        return selenium_test(sub_dir_path)