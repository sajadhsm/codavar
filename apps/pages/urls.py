from django.urls import path
from django.contrib.flatpages import views as flatpages_view

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Flat pages
    path('about/', flatpages_view.flatpage, {'url': '/about/'}, name='about'),
]
