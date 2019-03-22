"""codavar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.flatpages import views

from apps.contest.views import index as landing_view

urlpatterns = [
    path('', landing_view, name='index'),
    path('contest/', include('apps.contest.urls')),
    path('submission/', include('apps.submission.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    # Flat pages
    path('about/', views.flatpage, {'url': '/about/'}, name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)