from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contest/<int:contest_pk>/', views.ContestIndexView.as_view(), name='contest_index'),
    path('contest/<int:contest_pk>/problem/<int:problem_pk>/', views.contest_problem, name='contest_problem'),
    path('contest/<int:contest_pk>/submissions/', views.contest_submissions, name='contest_submissions'),
    path('contest/<int:contest_pk>/register/', views.contest_registeration, name='contest_registeration'),
    path('contest/<int:contest_pk>/leaderboard/', views.contest_leaderboard, name='contest_leaderboard'),
]