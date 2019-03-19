from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

class Contest(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    users = models.ManyToManyField(get_user_model(), related_name="contests", related_query_name="users", blank=True)

    def __str__(self):
        return self.name
    
    def has_started(self):
        return True if self.start_date < timezone.now() else False
    
    def has_ended(self):
        return True if self.end_date < timezone.now() else False
    
    @property
    def is_in_progress(self):
        return self.has_started() and not self.has_ended()
    
    @property
    def duration(self):
        return self.end_date - self.start_date