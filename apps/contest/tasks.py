import os
from celery import shared_task

from apps.submission.models import FrontEndContestSubmission

@shared_task
def run_selenium_test(submission_pk):
    """
    Extract submission zip
    Find the selenium script for given submission.problem
    Run the script and get the score
    Update submission.judge_score
    Set submission as final
    """
    submission = FrontEndContestSubmission.objects.get(pk=submission_pk)
    problem = submission.problem

    try:
        submission.extract()
    except:
        # TODO: Better error handeling (not catch all :|)
        submission.status = FrontEndContestSubmission.ERROR
        submission.save()
    else:
        # TODO:
        # If an exception raise inside the testscript, the unnitest will catch it
        # but the reason should be returned and let the user know about it
        # Also for now only the relative_score is returned
        relative_score = problem.run_selenium_script(submission.get_file_extract_path())
        submission.judge_score = int(relative_score * problem.score)
        submission.status = FrontEndContestSubmission.OK

        submission.set_as_final() # Calls save() internally