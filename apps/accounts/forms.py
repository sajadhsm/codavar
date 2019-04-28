from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name',)
    
class CustomUserEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=15, required=True)
    last_name = forms.CharField(max_length=15, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']

class SignupFormWithReCaptcha(SignupForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3, label="")
    field_order = ['email', 'password1', 'password2', 'captcha']
    
    def save(self, request):
        user = super(SignupFormWithReCaptcha, self).save(request)
        return user