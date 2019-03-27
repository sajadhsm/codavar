from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from apps.problem.models import FrontEndProblem
from apps.submission.models import FrontEndContestSubmission
from .models import FrontEndContest, FrontEndContestParticipation
from .decorators import check_contest_access
from .forms import FrontEndContestSubmissionForm
from .tasks import run_selenium_test
from .utils import get_contest_leaderboard

def index(request):
    contests = FrontEndContest.objects.all()
    return render(request, 'contest/index.html', {'contests': contests})

@login_required
@check_contest_access(FrontEndContest)
def contest_problem(request, contest_pk, problem_pk=None):
    contest = get_object_or_404(FrontEndContest, pk=contest_pk)
    if problem_pk:
        problem = FrontEndProblem.objects.get(pk=problem_pk)
    else:
        problem = contest.problems.first()

    if request.method == 'POST':
        if contest.is_in_progress:
            form = FrontEndContestSubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.contest = contest
                submission.problem = problem
                submission.user = request.user
                submission.save()
                run_selenium_test.delay(submission.pk)
                messages.success(request, 'Your code was uploaded successfully!')
                return redirect('contest_submissions', contest_pk)    
        else:
            # Don't allow form submission after contest is over
            raise PermissionDenied
    else:
        form = FrontEndContestSubmissionForm()
    
    return render(request, 'contest/contest.html', {
        'contest': contest,
        'problem': problem,
        'form': form
    })

@login_required
@check_contest_access(FrontEndContest)
def contest_submissions(request, contest_pk):
    contest = get_object_or_404(FrontEndContest, pk=contest_pk)
    user = request.user

    if not contest.participants.filter(pk=user.pk).exists():
        raise Http404
    
    submissions = FrontEndContestSubmission.objects.filter(user=user, contest=contest)
    return render(request, 'contest/contest_submissions.html', {
        'submissions': submissions,
        'contest': contest
    })

@login_required
@check_contest_access(FrontEndContest)
def set_as_final_sub(request, contest_pk, sub_pk):
    submission = get_object_or_404(FrontEndContestSubmission, pk=sub_pk, user=request.user)
    contest = submission.contest

    if not contest.is_in_progress:
        messages.error(request, "You can only set a submission as final during the contest!")
    elif (
        submission.status == FrontEndContestSubmission.PENDING or
        submission.status == FrontEndContestSubmission.ERROR
    ):
        messages.info(request, "This submission can't be set as final!")
    elif submission.is_final:
        messages.info(request, "This submission has been already set as final.")
    else:
        submission.set_as_final()
        messages.success(request, "The submission has been successfully set as final.")
    
    return redirect('contest_submissions', contest_pk)

@login_required
def contest_registration(request, contest_pk):
    contest = get_object_or_404(FrontEndContest, pk=contest_pk)

    if not contest.has_ended:
        user = request.user
        if not contest.participants.filter(pk=user.pk).exists():
            if user.first_name and user.last_name:
                FrontEndContestParticipation.objects.create(
                    participant=user,
                    contest=contest
                )
            else:
                messages.info(request, "Please set your first name and last name in-order to enter the contest!")
                return redirect('account_edit')
        
        if contest.has_started:
            return redirect('contest_index', contest_pk)

    return redirect('index')

@check_contest_access(FrontEndContest)
def contest_leaderboard(request, contest_pk):
    contest = get_object_or_404(FrontEndContest, pk=contest_pk)
    leaderboard = get_contest_leaderboard(contest)
    return render(
        request,
        'contest/contest_leaderboard.html',
        {
            'contest': contest,
            'leaderboard': leaderboard
        }
    )