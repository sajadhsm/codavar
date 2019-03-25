from django.db import models
from django.utils import timezone

class AbstractBaseContest(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_public = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ['-start_date']
    
    def __str__(self):
        return self.name

    @property
    def has_started(self):
        return True if self.start_date < timezone.now() else False
    @property
    def has_ended(self):
        return True if self.end_date < timezone.now() else False
    
    @property
    def is_in_progress(self):
        return self.has_started and not self.has_ended
    
    @property
    def duration(self):
        return self.end_date - self.start_date
