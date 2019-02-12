from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import PermissionDenied

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
def contest_index(request, contest_pk):
    contest = get_object_or_404(Contest, pk=contest_pk)
    problem = contest.problem_set.all().first()

    if request.method == 'POST':
        if contest.is_in_progress:
            form = SubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.problem = problem
                submission.user = request.user
                submission.save()

                run_selenium_test.delay(submission.pk)

                return redirect('contest_submissions', contest_pk)
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
def contest_problem(request, contest_pk, problem_pk):
    contest = get_object_or_404(Contest, pk=contest_pk)
    problem = Problem.objects.get(pk=problem_pk)

    if request.method == 'POST':
        if contest.is_in_progress:
            form = SubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.problem = problem
                submission.user = request.user
                submission.save()

                run_selenium_test.delay(submission.pk)

                return redirect('contest_submissions', contest_pk)    
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
    submissions = Submission.objects \
        .filter(user=request.user, problem__contest=contest_pk) \
        .order_by('-upload_date')
    return render(request, 'main/contest_submissions.html', {
        'submissions': submissions,
        'contest_pk': contest_pk
    })

@login_required
@contest_has_started
def set_as_final_sub(request, contest_pk, sub_pk):
    submission = get_object_or_404(Submission, pk=sub_pk, user=request.user)
    if not submission.is_final: submission.set_as_final()
    return redirect('contest_submissions', contest_pk)

@login_required
def contest_registration(request, contest_pk):
    contest = get_object_or_404(Contest, pk=contest_pk)

    if not contest.has_ended():
        user = request.user
        if not user.contests.filter(pk=contest_pk).exists():
            user.contests.add(contest)
            contest.users.add(user)
        
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