from django.contrib.auth.views import LoginView
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import path

from . import views
from .forms import UserPasswordChangeForm, UserPasswordResetForm, UserPasswordConfirmForm

urlpatterns = [
    path('sign-in/', LoginView.as_view(template_name='user_authentication/login.html'),
         name='login'),
    path('sign-out/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),

    # Profile
    path('<username>/profile/view/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.UpdateProfile.as_view(), name='update_profile'),

    # password change
    path('password/change/', PasswordChangeView.as_view(
        template_name="user_authentication/change_password.html",
        form_class=UserPasswordChangeForm),
         name='change_password'),

    path('password/change/done/', PasswordChangeDoneView.as_view(
        template_name='user_authentication/change_password_done.html'),
         name='password_change_done'),

    # password reset
    path('password/reset/', PasswordResetView.as_view(
        template_name='user_authentication/password_reset.html',
        form_class=UserPasswordResetForm),
         name='reset_password'),

    path('password/reset/done/', PasswordResetDoneView.as_view(
        template_name='user_authentication/password_reset_done.html'),
         name='password_reset_done'),

    path('password/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='user_authentication/password_reset_confirm.html',
        form_class=UserPasswordConfirmForm),
         name='password_reset_confirm'),

    path('password/reset/complete/', PasswordResetCompleteView.as_view(
        template_name='user_authentication/password_reset_complete.html'),
         name='password_reset_complete'),
]
