from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .decorators import contest_has_started
from .models import Contest, Problem, Submission
from .forms import SubmissionForm
from .tasks import run_selenium_test
from .utils import get_contest_leaderboard

def index(request):
    contests = Contest.objects.all()
    return render(request, 'main/index.html', {'contests': contests})

@login_required
@contest_has_started
def contest_problem(request, contest_pk, problem_pk=None):
    contest = get_object_or_404(Contest, pk=contest_pk)
    if problem_pk:
        problem = Problem.objects.get(pk=problem_pk)
    else:
        problem = contest.problem_set.first()

    if request.method == 'POST':
        if contest.is_in_progress:
            form = SubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                submission = form.save(commit=False)
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
        form = SubmissionForm()
    
    return render(request, 'main/contest.html', {
        'contest': contest,
        'problem': problem,
        'form': form
    })

@login_required
@contest_has_started
def contest_submissions(request, contest_pk):
    # Get the contest only for count-down
    # Better to find a work around to avoid this query
    contest = get_object_or_404(Contest, pk=contest_pk)
    submissions = Submission.objects \
        .filter(user=request.user, problem__contest=contest_pk) \
        .order_by('-upload_date')
    return render(request, 'main/contest_submissions.html', {
        'submissions': submissions,
        'contest': contest
    })

@login_required
@contest_has_started
def set_as_final_sub(request, contest_pk, sub_pk):
    submission = get_object_or_404(Submission, pk=sub_pk, user=request.user)
    # Don't set pending submissions as final
    if not submission.is_final and submission.judge_score != None:
        submission.set_as_final()
    return redirect('contest_submissions', contest_pk)

@login_required
def contest_registration(request, contest_pk):
    contest = get_object_or_404(Contest, pk=contest_pk)

    if not contest.has_ended():
        user = request.user
        if not user.contests.filter(pk=contest_pk).exists():
            if user.first_name and user.last_name:
                user.contests.add(contest)
                contest.users.add(user)
            else:
                messages.info(request, "Please set your first name and last name in-order to enter the contest!")
                return redirect('account_edit')
        
        if contest.has_started():
            return redirect('contest_index', contest_pk)

    return redirect('index')

@contest_has_started
def contest_leaderboard(request, contest_pk):
    contest = get_object_or_404(Contest, pk=contest_pk)
    leaderboard = get_contest_leaderboard(contest)
    return render(
        request,
        'main/contest_leaderboard.html',
        {
            'contest': contest,
            'leaderboard': leaderboard
        }
    )