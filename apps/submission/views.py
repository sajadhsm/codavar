from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Submission

@login_required
def submission_file_download(request, sub_pk):
    # TODO: Maybe better to be handle by web server according to:
    # https://stackoverflow.com/a/7304609
    submission = get_object_or_404(Submission, pk=sub_pk)

    if request.user == submission.user:
        with open(submission.zip_file.path, 'rb') as file:
            response = HttpResponse(file, content_type='application/zip')
            file_name = submission.zip_file.name.split('/')[-1]
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response
    else:
        raise Http404