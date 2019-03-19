from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserEditForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'accounts/signup.html', {'form': form})

def edit_user_view(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your information were updated successfully!')
            return redirect('account_edit')
    else:
        form = CustomUserEditForm(instance=request.user)
    
    return render(request, 'accounts/edit.html', {'form': form})