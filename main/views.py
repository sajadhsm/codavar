from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from .models import Contest, Problem, Submission
from .forms import SubmissionForm

def index(request):
    contests = Contest.objects.all()
    return render(request, 'main/index.html', {'contests': contests})

class ContestIndexView(View):
    def render(self, request):
        return render(request, 'main/contest.html', {
            'contest': self.contest,
            'problem': self.problem,
            'form': self.form
        })
    
    def post(self, request, *args, **kwargs):
        self.contest = get_object_or_404(Contest, pk=self.kwargs['contest_pk'])
        problem_pk = self.contest.problem_set.all()[0].pk
        self.problem = Problem.objects.get(pk=problem_pk)
        self.form = SubmissionForm(request.POST, request.FILES)
        if self.form.is_valid():
            submission = self.form.save(commit=False)
            submission.problem = self.problem
            submission.user = request.user
            submission.save()

            return redirect('contest_submissions', self.kwargs['contest_pk'])

    def get(self, request, *args, **kwargs):
        self.contest = get_object_or_404(Contest, pk=self.kwargs['contest_pk'])
        problem_pk = self.contest.problem_set.all()[0].pk
        self.problem = Problem.objects.get(pk=problem_pk)
        self.form = SubmissionForm()

        return self.render(request)


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

            return redirect('contest_submissions', contest_pk)
        
    else:
        form = SubmissionForm()
    
    return render(request, 'main/contest.html', {
        'contest': contest,
        'problem': problem,
        'form': form
    })

def contest_submissions(request, contest_pk):
    submissions = Submission.objects.filter(user=request.user)
    return render(request, 'main/contest_submissions.html', {'submissions': submissions})