from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path

from . import views
from .forms import UserPasswordChangeForm

urlpatterns = [
    path('sign-in/', LoginView.as_view(template_name='user_authentication/login.html'),
         name='login'),
    path('sign-out/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),

    # Profile
    path('profile/update/', views.UpdateProfile.as_view(), name='update_profile'),

    # password change
    path('password/change/', PasswordChangeView.as_view(
        template_name="user_authentication/change_password.html",
        form_class=UserPasswordChangeForm),
         name='change_password'),

    path('password/change/done/', PasswordChangeDoneView.as_view(
        template_name='user_authentication/password_change_done.html'),
         name='password_change_done'),
]
