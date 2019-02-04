from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contest/<int:contest_pk>/', views.contest_index, name='contest_index'),
    path('contest/<int:contest_pk>/problem/<int:problem_pk>/', views.contest_problem, name='contest_problem'),
]