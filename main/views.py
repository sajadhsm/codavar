from django.shortcuts import get_object_or_404, redirect, render

from django.db.models import Sum, Case, When, IntegerField

from django.contrib.auth.decorators import login_required
from .decorators import contest_has_started

from .models import Contest, Problem, Submission
from .forms import SubmissionForm
from .tasks import run_selenium_test

def index(request):
    contests = Contest.objects.all()
    return render(request, 'main/index.html', {'contests': contests})

@login_required
@contest_has_started
def contest_index(request, contest_pk):
    contest = get_object_or_404(Contest, pk=contest_pk)
    problem = contest.problem_set.all().first()

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.problem = problem
            submission.user = request.user
            submission.save()

            run_selenium_test.delay(submission.pk)

            return redirect('contest_submissions', contest_pk)
        
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
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.problem = problem
            submission.user = request.user
            submission.save()

            run_selenium_test.delay(submission.pk)

            return redirect('contest_submissions', contest_pk)
        
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
    # There should be a better approuch to retrive
    # final submission and gather everthing into a single
    # queryset but for now it's working...! :)

    # TODO: Improve queryset

    contest = get_object_or_404(Contest, pk=contest_pk)

    contest_subs = Submission.objects.filter(
        problem__contest=contest,
        is_final=True)

    users = contest.users.annotate(total_score=Sum(
        Case(When(
                submission__is_final=True,
                submission__in=contest_subs,
                then='submission__judge_score'
            ),
            output_field=IntegerField()
        ))).order_by('-total_score')

    return render(
        request,
        'main/contest_leaderboard.html',
        {
            'contest': contest,
            'users': users,
            'contest_subs': contest_subs
        }
    )