from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from apps.problem.models import FrontEndProblem
from apps.submission.models import FrontEndContestSubmission
from .models import FrontEndContest, FrontEndContestParticipation
from .decorators import check_contest_access
from .forms import FrontEndContestSubmissionForm
from .tasks import run_selenium_test
from .utils.leaderboard import get_contest_leaderboard

@login_required
@check_contest_access(FrontEndContest)
def contest_problem(request, contest_pk, problem_pk=None):
    contest = get_object_or_404(FrontEndContest, pk=contest_pk)
    if problem_pk:
        problem = FrontEndProblem.objects.get(pk=problem_pk)
    else:
        problem = contest.problems.first()

    if request.method == 'POST':
        if contest.is_in_progress or request.user.is_staff:
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
    
    # TODO: Make it optimized!
    # Lots of calculations are happening here for a colored badge in the front-end :\
    contest_problems = []
    for prob in contest.problems.all():
        has_user_solved_problem = FrontEndContestSubmission.objects.filter(
            user=request.user,
            contest=contest,
            problem=prob,
            relative_score__gte=1.0
        ).exists()

        contest_problems.append({
            "problem": prob,
            "solved": bool(has_user_solved_problem)
        })
    
    return render(request, 'contest/contest.html', {
        'contest': contest,
        'contest_problems': contest_problems,
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
    
    all_submissions = FrontEndContestSubmission.objects.filter(user=user, contest=contest)
    paginator = Paginator(all_submissions, 12)
    page = request.GET.get('page', 1)

    try:
        submissions = paginator.page(page)
    except PageNotAnInteger:
        submissions = paginator.page(1)
    except EmptyPage:
        submissions = paginator.page(paginator.num_pages)
        
    return render(request, 'contest/contest_submissions.html', {
        'submissions': submissions,
        'contest': contest
    })

@login_required
@check_contest_access(FrontEndContest)
def set_as_final_sub(request, contest_pk, sub_pk):
    submission = get_object_or_404(FrontEndContestSubmission, pk=sub_pk, user=request.user)
    contest = submission.contest

    if request.user.is_staff:
        # TODO: Use a better condition for STAFFs
        # Currently the PENDING/ERROR or ALREADY FINAL subs can be set as final for STAFFs
        submission.set_as_final()
        messages.success(request, "The submission has been successfully set as final.")
    elif not contest.is_in_progress:
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

    # Different than @check_contest_access(FrontEndContest)
    if not (request.user.is_staff or contest.is_public):
        raise Http404

    if not contest.has_ended:
        user = request.user
        if not contest.participants.filter(pk=user.pk).exists():
            if user.first_name and user.last_name:
                FrontEndContestParticipation.objects.create(
                    participant=user,
                    contest=contest
                )
            else:
                messages.info(request, "Please set your <b>first name</b> and <b>last name</b> in order to register in the contest.")
                return redirect('account_edit', contest_pk)
        
        if contest.has_started:
            return redirect('contest_index', contest_pk)
        else:
            messages.success(request, "You have been added to contest participants list. Please wait for the contest to begins.")

    return redirect('index')

@check_contest_access(FrontEndContest)
def contest_leaderboard(request, contest_pk):
    contest = get_object_or_404(FrontEndContest, pk=contest_pk)
    leaderboard_list = get_contest_leaderboard(contest)

    paginator = Paginator(leaderboard_list, 50)
    page = request.GET.get('page', 1)
    
    try:
        leaderboard = paginator.page(page)
    except PageNotAnInteger:
        leaderboard = paginator.page(1)
    except EmptyPage:
        leaderboard = paginator.page(paginator.num_pages)

    return render(
        request,
        'contest/contest_leaderboard.html',
        {
            'contest': contest,
            'leaderboard': leaderboard
        }
    )