from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit/', views.edit_user_view, name='account_edit'),
    path('change-password/', views.change_password, name='change_password'),
]