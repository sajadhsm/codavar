import importlib

from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .abstract_base_problem import AbstractBaseProblem

selenium_scripts_storage = FileSystemStorage(
    location=settings.SELENIUM_SCRIPT_ROOT,
    base_url=settings.SELENIUM_SCRIPT_URL
)

def selenium_script_filename(instance, filename):
    problem_name = instance.title.replace(" ", "_")
    file_name = filename.replace(" ", "_")
    return "{}__{}".format(problem_name, file_name)

class FrontEndProblem(AbstractBaseProblem):
    score = models.PositiveIntegerField(default=1)
    selenium_script = models.FileField(
        upload_to=selenium_script_filename,
        storage=selenium_scripts_storage,
        blank=True
    )

    class Meta:
        ordering = ['score']
    
    def selenium_script_as_module_string(self):
        return '.{}'.format(str(self.selenium_script).split('.py')[0])

    def run_selenium_script(self, sub_dir_path):
        script_module = importlib.import_module(
            self.selenium_script_as_module_string(),
            package=settings.SELENIUM_SCRIPT_IMPORT_MODULE_PACKAGE)
        run_test = script_module.run_test
        return run_test(sub_dir_path)