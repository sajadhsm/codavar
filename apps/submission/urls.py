from django.urls import path

from . import views

urlpatterns = [
    path('<int:sub_pk>/download/', views.submission_file_download, name='submission_file_download'),
]