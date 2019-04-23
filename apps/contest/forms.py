import magic

from django.forms import ModelForm
from django.core.exceptions import ValidationError

from apps.submission.models import FrontEndContestSubmission

SUBMISSION_ZIP_MAX_SIZE = 2097152 #2MB

class FrontEndContestSubmissionForm(ModelForm):
    def clean_file(self):
        # Maybe validation should be defined at Model level
        # But this way we can have different types of forms
        # with different validations... IDK
        file = self.cleaned_data.get("file")
        filetype = magic.from_buffer(file.read(), mime=True)
        
        if not "application/zip" in filetype:
            raise ValidationError('File is not ZIP.', code='invalid')
        
        # TODO: It would be much more interesting if the max file size
        # is fetched from the related problem because there may be a problem
        # that require a bigger file!! [But it's a bit tricky to implement]
        # Submission problem has not been bounded yet... So it may be possible
        # if problem.pk is passed to this form as argument and retrived mannualy
        # so we can read the max_file_size and ...
        if file.size > SUBMISSION_ZIP_MAX_SIZE:
            raise ValidationError('File size is greater than 2MB.', code='invalid')
        return file

    class Meta:
        model = FrontEndContestSubmission
        fields = ['file']