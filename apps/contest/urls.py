from django.urls import path

from . import views

urlpatterns = [
    path('<int:contest_pk>/', views.contest_problem, name='contest_index'),
    path('<int:contest_pk>/problem/<int:problem_pk>/', views.contest_problem, name='contest_problem'),
    path('<int:contest_pk>/submissions/', views.contest_submissions, name='contest_submissions'),
    path('<int:contest_pk>/submissions/<int:sub_pk>/', views.set_as_final_sub, name='set_as_final_sub'),
    path('<int:contest_pk>/register/', views.contest_registration, name='contest_registration'),
    path('<int:contest_pk>/leaderboard/', views.contest_leaderboard, name='contest_leaderboard'),
]
