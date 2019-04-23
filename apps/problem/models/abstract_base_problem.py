from django.db import models

class AbstractBaseProblem(models.Model):
    title = models.CharField(max_length=200)
    statement = models.TextField()
    is_public = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title