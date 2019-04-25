from django.urls import include, path

from . import views

urlpatterns = [
    path('', include('allauth.urls')),
    path('edit/', views.edit_user_view, name='account_edit'),
    path('edit/<int:contest_pk>/', views.edit_user_view, name='account_edit'),
]