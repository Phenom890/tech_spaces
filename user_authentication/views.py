from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.views import View

from .forms import UserRegisterForm, UserUpdateForm


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
            return redirect('home') #FIXME:change this redirect to user profile
        messages.error(request, 'Fill the forms correctly!')

        context = {
            'form': form,
        }
        return render(request, 'user_authentication/profile_update.html', context)

