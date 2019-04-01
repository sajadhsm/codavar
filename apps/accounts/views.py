from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from .models import CustomUser
from .forms import CustomUserEditForm

@login_required
def edit_user_view(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your information were updated successfully!')
            return redirect('account_edit')
        else:
            messages.error(request, 'Please correct the error(s) below.')
    else:
        form = CustomUserEditForm(instance=request.user)
    
    return render(request, 'accounts/edit.html', {'form': form})
    