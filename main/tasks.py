from celery import shared_task

from .models import Submission

@shared_task
def run_selenium_test(submission_pk):
    """
    Extract submission zip
    Find the selenium script for given submission.problem
    Run the script and get the score
    Update submission.judge_score
    Save submission
    """
    submission = Submission.objects.get(pk=submission_pk)
    problem = submission.problem

    submission.extract()
    sub_extracted_dir = submission.zip_file.path[:-4]
    score = problem.run_selenium_script(sub_extracted_dir)
    
    submission.judge_score = score
    submission.save()