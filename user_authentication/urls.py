from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('sign-in/', LoginView.as_view(template_name='user_authentication/login.html'), name='login'),
    path('sign-out/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
]