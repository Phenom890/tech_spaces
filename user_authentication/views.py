from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from core.models import User
from .forms import UserRegisterForm, UserUpdateForm


# TODO:fix the profile page

class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()

        context = {
            "form": form,
        }
        return render(request, 'user_authentication/register.html', context)

    def post(self, request):
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully!')
            return redirect('login')

        context = {
            'form': form,
        }
        return render(request, 'user_authentication/register.html', context)


class UserLogoutView(View):
    def get(self, request):
        return render(request, 'user_authentication/logout.html')

    def post(self, request):
        return LogoutView.as_view(next_page='login')(request)


class UpdateProfile(View):
    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        context = {
            'form': form,
        }
        return render(request, 'user_authentication/profile_update.html', context)

    def post(self, request):
        form = UserUpdateForm(request.POST or None, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated Successfully!')
            return redirect('profile', username=request.user.username)
        messages.error(request, 'Fill the forms correctly!')

        context = {
            'form': form,
        }
        return render(request, 'user_authentication/profile_update.html', context)


class ProfileView(View):
    def get(self, request, username):
        get_user = get_object_or_404(User, username=username)
        user_answers = get_user.answer_set.all()
        user_questions = get_user.question_set.all()
        context = {
            'user': get_user,
            'query_questions': user_questions,
            'student_answers': user_answers,
        }
        return render(request, 'user_authentication/profile.html', context)
