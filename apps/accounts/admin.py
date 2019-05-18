from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser

    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined',)
    list_filter = ('date_joined', 'is_staff', 'is_active',)

    readonly_fields = ('date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'date_joined')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active')}
        ),
    )
    
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('-date_joined',)

admin.site.register(CustomUser, CustomUserAdmin)
