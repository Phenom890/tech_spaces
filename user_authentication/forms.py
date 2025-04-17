from django import forms
from django.contrib.auth.forms import (
    PasswordChangeForm,
    UserCreationForm,
    PasswordResetForm,
    SetPasswordForm
)

from core.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )
    new_password1 = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )


class UserPasswordResetForm(PasswordResetForm):
    email = forms.CharField(label='Email', max_length=200, widget=forms.EmailInput())


class UserPasswordConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New Password', max_length=200,
        widget=forms.PasswordInput(
            attrs={'auto-complete': 'current-password'}
        ),
    )
    new_password2 = forms.CharField(
        label='Confirm New Password', max_length=200,
        widget=forms.PasswordInput(
            attrs={'auto-complete': 'current-password'}
        ),
    )
