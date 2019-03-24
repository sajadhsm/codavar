import secrets

from django.db import models
from django.contrib.auth import get_user_model

def generate_filename(instance, filename):
    # Makes it a little harder to guess the file location for end user
    # by using random secret token
    # TODO: But it's still possible for every one to download the file
    # if they find the actual file URL
    # Maybe try: https://github.com/edoburu/django-private-storage
    return f'submissions/{secrets.token_urlsafe(10)}/{filename}'

class AbstractBaseSubmission(models.Model):
    file = models.FileField(upload_to=generate_filename)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f'By {self.user.email} at {self.upload_date}'