import magic

from django.forms import ModelForm
from django.core.exceptions import ValidationError

from apps.submission.models import Submission

SUBMISSION_ZIP_MAX_SIZE = 2097152 #2MB

class SubmissionForm(ModelForm):
    def clean_zip_file(self):
        file = self.cleaned_data.get("zip_file")
        filetype = magic.from_buffer(file.read(), mime=True)
        
        if not "application/zip" in filetype:
            raise ValidationError('File is not ZIP.', code='invalid')
        
        if file.size > SUBMISSION_ZIP_MAX_SIZE:
            raise ValidationError('File size is greater than 2MB.', code='invalid')
        return file

    class Meta:
        model = Submission
        fields = ['zip_file']