from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.views import View

from .forms import UserRegisterForm


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
