import os
from celery import shared_task

from apps.submission.models import FrontEndContestSubmission

@shared_task
def run_selenium_test(submission_pk):
    """
    Extracts the submission and run the selenium tests and
    updates the submission.

    If the submission gets a higher score than current problem
    final sub, it will set as final automaticlly.
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
        judge_score = int(relative_score * problem.score)
        submission.judge_score = judge_score
        submission.status = FrontEndContestSubmission.OK

        current_final = FrontEndContestSubmission.objects.filter(
            is_final=True,
            problem=problem,
            contest=submission.contest
        ).first()

        if not current_final or judge_score > current_final.judge_score:
            submission.set_as_final() # Calls save() internally
        else:
            submission.save()