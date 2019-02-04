from django.shortcuts import get_object_or_404, render

from .models import Contest, Problem

def index(request):
    contests = Contest.objects.all()
    return render(request, 'main/index.html', {'contests': contests})

def contest_index(request, contest_pk):
    contest = get_object_or_404(Contest, pk=contest_pk)
    problem_pk = contest.problem_set.all()[0].pk
    problem = Problem.objects.get(pk=problem_pk)
    
    return render(request, 'main/contest.html', {
        'contest': contest,
        'problem': problem
    })

def contest_problem(request, contest_pk, problem_pk):
    contest = get_object_or_404(Contest, pk=contest_pk)
    problem = Problem.objects.get(pk=problem_pk)
    
    return render(request, 'main/contest.html', {
        'contest': contest,
        'problem': problem
    })